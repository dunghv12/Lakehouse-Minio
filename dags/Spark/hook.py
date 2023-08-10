from airflow.providers.apache.spark.hooks.spark_submit import SparkSubmitHook
from airflow.exceptions import AirflowException
import contextlib
import os
import re
import subprocess
import time
from typing import Any, Iterator

class CustomHook(SparkSubmitHook):
    def _build_track_driver_status_command(self) -> list[str]:
        """
        Construct the command to poll the driver status.

        :return: full command to be executed
        """
        curl_max_wait_time = 30
        spark_host = self._connection["master"]
        if spark_host.endswith(":6066"):
            spark_host = spark_host.replace("spark://", "http://")
            connection_cmd = [
                "/usr/bin/curl",
                "--max-time",
                str(curl_max_wait_time),
                f"{spark_host}/v1/submissions/status/{self._driver_id}",
            ]
            self.log.info(connection_cmd)

            # The driver id so we can poll for its status
            if not self._driver_id:
                raise AirflowException(
                    "Invalid status: attempted to poll driver status but no driver id is known. Giving up."
                )

        else:
            spark_host = spark_host.replace("spark://", "http://").replace("7077","6066")
            connection_cmd = [
                "/usr/bin/curl",
                "--max-time",
                str(curl_max_wait_time),
                f"{spark_host}/v1/submissions/status/{self._driver_id}",
            ]
            self.log.info(connection_cmd)

            # The driver id so we can poll for its status
            if not self._driver_id:
                raise AirflowException(
                    "Invalid status: attempted to poll driver status but no driver id is known. Giving up."
                )

        self.log.info("Poll driver status cmd run test!!!!!!!!!!!!!!!!!!!!!!!!!: %s", connection_cmd)

        return connection_cmd

    def _start_driver_status_tracking(self) -> None:
        """
        Polls the driver based on self._driver_id to get the status.
        Finish successfully when the status is FINISHED.
        Finish failed when the status is ERROR/UNKNOWN/KILLED/FAILED.

        Possible status:

        SUBMITTED
            Submitted but not yet scheduled on a worker
        RUNNING
            Has been allocated to a worker to run
        FINISHED
            Previously ran and exited cleanly
        RELAUNCHING
            Exited non-zero or due to worker failure, but has not yet
            started running again
        UNKNOWN
            The status of the driver is temporarily not known due to
            master failure recovery
        KILLED
            A user manually killed this driver
        FAILED
            The driver exited non-zero and was not supervised
        ERROR
            Unable to run or restart due to an unrecoverable error
            (e.g. missing jar file)
        """
        # When your Spark Standalone cluster is not performing well
        # due to misconfiguration or heavy loads.
        # it is possible that the polling request will timeout.
        # Therefore we use a simple retry mechanism.
        missed_job_status_reports = 0
        max_missed_job_status_reports = 10

        # Keep polling as long as the driver is processing
        while self._driver_status not in ["FINISHED", "UNKNOWN", "KILLED", "FAILED", "ERROR"]:
            # Sleep for n seconds as we do not want to spam the cluster
            time.sleep(self._status_poll_interval)

            self.log.debug("polling status of spark driver with id %s", self._driver_id)

            poll_drive_status_cmd = self._build_track_driver_status_command()
            status_process: Any = subprocess.Popen(
                poll_drive_status_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=-1,
                universal_newlines=True,
            )
            self._process_spark_status_log(iter(status_process.stdout))
            returncode = status_process.wait()
            self.log.info("Driver check status!!!!!!!!!!!!!!!!!!!!!!!!!: %s", returncode)
            if returncode:
                if missed_job_status_reports < max_missed_job_status_reports:
                    missed_job_status_reports += 1
                else:
                    raise AirflowException(
                        f"Failed to poll for the driver status {max_missed_job_status_reports} times: "
                        f"returncode = {returncode}"
                    )
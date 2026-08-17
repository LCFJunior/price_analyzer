import time
from collections.abc import Callable


class MonitorScheduler:
    def __init__(
        self,
        interval_seconds: int,
        task: Callable[[], None],
    ):
        if interval_seconds < 60:
            raise ValueError(
                "O intervalo mínimo deve ser de 60 segundos."
            )

        self.interval_seconds = interval_seconds
        self.task = task

    def run_forever(self) -> None:
        print(
            "Monitor iniciado. Intervalo: "
            f"{self.interval_seconds} segundos."
        )

        while True:
            started_at = time.time()

            try:
                self.task()
            except KeyboardInterrupt:
                print("\nMonitor encerrado pelo usuário.")
                break
            except Exception as error:
                print(
                    "\nErro durante a coleta: "
                    f"{type(error).__name__}: {error}"
                )

            elapsed = time.time() - started_at
            waiting_time = max(
                0,
                self.interval_seconds - elapsed,
            )

            print(
                "\nPróxima coleta em "
                f"{waiting_time:.0f} segundos."
            )

            try:
                time.sleep(waiting_time)
            except KeyboardInterrupt:
                print("\nMonitor encerrado pelo usuário.")
                break
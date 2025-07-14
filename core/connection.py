import subprocess
import psutil
import time
from PyQt6.QtCore import QObject, QThread, pyqtSignal

from utils.network import find_available_port


class ConnectionWorker(QThread):
    """
    Worker thread to handle the Shadowsocks connection process and health check.
    """
    finished = pyqtSignal(bool, str, int, str)

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.local_port = 1080
        self.process = None

    def run(self):
        """Starts ss-local, then performs a health check."""
        server_id = self.config.get("id")
        try:
            self.local_port = find_available_port(1080)
            command = [
                'ss-local', '-s', self.config['server'], '-p', str(self.config['server_port']),
                '-l', str(self.local_port), '-k', self.config['password'], '-m', self.config['method']
            ]
            self.process = subprocess.Popen(command, stderr=subprocess.PIPE, text=True)

            time.sleep(0.75)

            if self.process.poll() is not None:
                raise Exception(self.process.stderr.read() or "Process terminated unexpectedly.")

            self.health_check()

            self.finished.emit(True, f"Connected on port {self.local_port}", self.local_port, server_id)

        except Exception as e:
            self.stop_process()
            error_msg = f"Connection Failed. Please check server details.\n\n<i style='color:#78909C'>Details: {e}</i>"
            self.finished.emit(False, error_msg, self.local_port, server_id)

    def health_check(self):
        """Uses curl to test connectivity through the new proxy."""
        print(f"Health check: Pinging through port {self.local_port}")
        curl_command = [
            'curl', '--socks5-hostname', f'127.0.0.1:{self.local_port}',
            '--head', '--connect-timeout', '5', 'https://www.google.com'
        ]
        result = subprocess.run(curl_command, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(result.stderr or "Connection Refused by remote server.")

    def stop_process(self):
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None

    def stop(self):
        self.stop_process()
        self.requestInterruption()
        self.quit()


class ConnectionManager(QObject):
    """Manages the connection worker thread lifecycle. Inherits from QObject to handle signals."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.local_port = 1080

    def connect(self, config, callback):
        self.disconnect()
        self.worker = ConnectionWorker(config)
        self.worker.finished.connect(callback)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    def on_worker_finished(self):
        """Slot to clear the worker reference after it's done."""
        self.worker = None

    def disconnect(self):
        """Stops the worker and kills any orphaned ss-local processes."""
        print("Stopping Shadowsocks connection...")
        if self.worker and self.worker.isRunning():
            self.worker.stop()

        for proc in psutil.process_iter(['pid', 'name']):
            if 'ss-local' in proc.info['name']:
                try:
                    p = psutil.Process(proc.info['pid'])
                    p.terminate()
                    p.wait(timeout=1)
                    print(f"Terminated orphaned ss-local process with PID {proc.info['pid']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                    pass
        self.worker = None

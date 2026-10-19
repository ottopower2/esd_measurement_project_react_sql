from pathlib import Path
from datetime import datetime
import base64

from config import MOCK_SCOPE, SCOPE_IP

# 1x1 PNG, used only in mock mode so the full app works without an oscilloscope.
MOCK_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


class ScopeClient:
    def __init__(self, ip: str = SCOPE_IP, mock: bool = MOCK_SCOPE):
        self.ip = ip
        self.mock = mock
        self.scope = None

        if not self.mock:
            import pyvisa

            rm = pyvisa.ResourceManager()
            self.scope = rm.open_resource(f"TCPIP::{self.ip}::INSTR")
            self.scope.timeout = 10000 # 10 seconds timeout for long operations like screenshots
            self.configure_scope()

    def get_identity(self) -> str:
        if self.mock:
            return "MOCK Rohde&Schwarz RTO6"
        return self.scope.query("*IDN?").strip()

    def configure_scope(self):
        if self.mock:
            return

        # Basic scope setup for real hardware. Adapt these SCPI commands
        # to your oscilloscope model and the active measurement setup.
        self.scope.write("SYST:LANG SCPI")
        self.scope.write("CHAN1:DISP ON")
        self.scope.write("MEASUrement1:TYPE VOLTage")
        self.scope.write("MEASUrement1:VOLTage:FUNC RESult")
        self.scope.query("*OPC?")

    def get_voltage(self) -> float:
        if self.mock:
            return 7.52

            # peak-to-peak voltage, adjust to your test setup
        self.scope.write("MEASUrement1:VOLTage:FUNC RESult")
        self.scope.write("MEASUrement1:VOLTage:RESult:TYPE PK2pk")

        # Adjust this SCPI command to the measurement configured on your RTO6/RTM64.
        value = self.scope.query("MEASurement1:RESult:ACTual?")
        return float(value)

    def save_screenshot(self, local_path: str) -> str:
        path = Path(local_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if self.mock:
            path.write_bytes(MOCK_PNG)
            return str(path)

        remote_name = f"C:\\Temp\\esd_{datetime.now():%Y%m%d_%H%M%S}.png"
        self.scope.write("HCOPy:DEVice:LANGuage PNG")
        self.scope.write(f"MMEMory:NAME '{remote_name}'")
        self.scope.write("HCOPy:IMMediate")

        data = self.scope.query_binary_values(
            f"MMEMory:DATA? '{remote_name}'",
            datatype="B",
            container=bytes,
        )
        path.write_bytes(data)
        return str(path)

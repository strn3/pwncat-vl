#!/usr/bin/env python3
import pwncat
from pwncat.facts.windows import ProcessTokenPrivilege
from pwncat.modules import ModuleFailed
from pwncat.modules.enumerate import EnumerateModule, Schedule, Scope
from pwncat.platform.windows import PowershellError, Windows


class Module(EnumerateModule):
    """Locate process privileges"""

    PLATFORM = [Windows]
    SCHEDULE = Schedule.PER_USER
    SCOPE = Scope.SESSION
    PROVIDES = ["token.privilege"]

    def enumerate(self, session: "pwncat.manager.Session"):
        """Check for privileges"""

        # Load PowerUp.ps1
        session.run("powersploit", group="privesc")

        try:
            privs = session.platform.powershell("Get-ProcessTokenPrivilege")[0]
        except (IndexError, PowershellError) as exc:
            raise ModuleFailed(f"failed to find process token privs: {exc}") from exc

        for priv in privs:
            yield ProcessTokenPrivilege(
                source=self.name,
                name=priv["Privilege"],
                attributes=priv["Attributes"],
                handle=priv["TokenHandle"],
                pid=priv["ProcessId"],
            )

import pwncat
from pwncat.facts.linux import LinuxGroup
from pwncat.modules import ModuleFailed, Status
from pwncat.modules.enumerate import EnumerateModule, Schedule
from pwncat.platform.linux import Linux


class Module(EnumerateModule):
    """Enumerate users from a linux target"""

    PROVIDES = ["group"]
    PLATFORM = [Linux]
    SCHEDULE = Schedule.ONCE

    def enumerate(self, session: "pwncat.manager.Session"):

        # Grab all the users and sort by their group ID
        users = {user.gid: user for user in session.run("enumerate", types=["user"])}

        group_file = session.platform.Path("/etc/group")
        groups = []

        try:
            with group_file.open("r") as filp:
                for group_line in filp:
                    try:
                        # Extract the group fields
                        group_name, hash, gid, members = group_line.split(":")
                        gid = int(gid)
                        members = [m.strip() for m in members.split(",") if m.strip()]

                        if gid in users:
                            members.append(users[gid].name)

                        # Build a group object
                        groups.append(
                            LinuxGroup(self.name, group_name, hash, gid, members),
                        )

                        yield Status(group_name)

                    except (KeyError, ValueError, IndexError):
                        # Bad group line
                        continue

            yield from groups

        except (FileNotFoundError, PermissionError) as exc:
            raise ModuleFailed(str(exc)) from exc

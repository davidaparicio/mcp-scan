import sys
import argparse
from .MCPScanner import MCPScanner
import rich
from .version import version_info


def str2bool(v):
    return v.lower() in ("true", "1", "t", "y", "yes")


if sys.platform == "linux" or sys.platform == "linux2":
    WELL_KNOWN_MCP_PATHS = [
        "~/.codeium/windsurf/mcp_config.json",  # windsurf
        "~/.cursor/mcp.json",  # cursor
        "~/.vscode/mcp.json",  # vscode
        "~/.config/Code/User/settings.json",  # vscode linux
    ]
elif sys.platform == "darwin":
    # OS X
    WELL_KNOWN_MCP_PATHS = [
        "~/.codeium/windsurf/mcp_config.json",  # windsurf
        "~/.cursor/mcp.json",  # cursor
        "~/Library/Application Support/Claude/claude_desktop_config.json",  # Claude Desktop mac
        "~/.vscode/mcp.json",  # vscode
        "~/Library/Application Support/Code/User/settings.json",  # vscode mac
    ]
elif sys.platform == "win32":
    WELL_KNOWN_MCP_PATHS = [
        "~/.codeium/windsurf/mcp_config.json",  # windsurf
        "~/.cursor/mcp.json",  # cursor
        "~/AppData/Roaming/Claude/claude_desktop_config.json",  # Claude Desktop windows
        "~/.vscode/mcp.json",  # vscode
        "~/AppData/Roaming/Code/User/settings.json",  # vscode windows
    ]
else:
    WELL_KNOWN_MCP_PATHS = []


def main():
    parser = argparse.ArgumentParser(description="MCP-scan CLI")
    parser.add_argument(
        "--checks-per-server",
        type=int,
        default=1,
        help="Number of checks to perform on each server, values greater than 1 help catch non-deterministic behavior",
    )
    parser.add_argument(
        "--storage-file",
        type=str,
        default="~/.mcp-scan",
        help="Path to previous scan results",
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default="https://mcp.invariantlabs.ai/",
        help="Base URL for the checking server",
    )
    parser.add_argument(
        "--server-timeout",
        type=float,
        default=10,
        help="Number of seconds to wait while trying a mcp server",
    )
    parser.add_argument(
        "--suppress-mcpserver-io",
        default=True,
        type=str2bool,
        help="Suppress the output of the mcp server",
    )
    parser.add_argument(
        "files",
        type=str,
        nargs="*",
        default=WELL_KNOWN_MCP_PATHS,
        help="Different file locations to scan. This can include custom file locations as long as they are in an expected format, including Claude, Cursor or VSCode format.",
    )

    rich.print("[bold blue]Invariant MCP-scan v{}[/bold blue]\n".format(version_info))

    args = parser.parse_args()

    # print help
    if len(sys.argv) == 2 and sys.argv[1] == "help":
        parser.print_help()
        sys.exit(0)

    # check for case where the only file is 'inspect'
    if len(sys.argv) == 2 and sys.argv[1] == "inspect":
        args.files = WELL_KNOWN_MCP_PATHS
        MCPScanner(**vars(args)).inspect()
        sys.exit(0)

    scanner = MCPScanner(**vars(args))
    scanner.start()

    sys.exit(0)


if __name__ == "__main__":
    main()

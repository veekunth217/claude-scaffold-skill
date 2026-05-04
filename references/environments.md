# Environment Detection Reference

This file is loaded on-demand by the scaffolding wizard to handle edge cases in environment detection.

---

## Detection Logic

### Docker Container
```bash
[ -f /.dockerenv ] && echo "docker"
```
Also check: `cat /proc/1/cgroup 2>/dev/null | grep docker`

**Implications for scaffolding:**
- No GUI tools (no browser-based setup wizards)
- May not have sudo access
- Package manager is whatever the base image uses (usually apt for Debian/Ubuntu images)
- Prefer `apt-get` over `apt` for scripts (more stable output)
- Volumes may be mounted — check before writing to `/app` or `/workspace`

### VPS / Headless Server
```bash
[ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ] && echo "headless"
```

**Implications for scaffolding:**
- No desktop package managers (no `brew`, no `choco`)
- Check if user has sudo: `sudo -n true 2>/dev/null && echo "has_sudo" || echo "no_sudo"`
- Prefer non-interactive installs: `apt-get install -y`
- Web servers need firewall rules — remind user: `ufw allow 80`, `ufw allow 443`
- For Node/Python: version managers are strongly preferred over system packages

### Mac (Local)
```bash
uname -s | grep -q Darwin && echo "mac"
```
- Homebrew is the preferred package manager
- Check if Xcode CLI tools are installed: `xcode-select -p 2>/dev/null`
- If missing: `xcode-select --install`
- Apple Silicon (M1/M2/M3): `uname -m` returns `arm64` — some older tools have compatibility issues

### Linux (Local Desktop)
```bash
uname -s | grep -q Linux && [ -n "$DISPLAY" ] && echo "linux_desktop"
```
- Check distro: `cat /etc/os-release | grep ^ID=`
- Ubuntu/Debian: apt
- Fedora/RHEL/CentOS: dnf or yum
- Arch: pacman
- openSUSE: zypper

### Windows (WSL)
```bash
uname -r | grep -qi microsoft && echo "wsl"
```
- File paths: use Linux paths within WSL (`/home/user/`) but Windows paths for files shared with Windows (`/mnt/c/`)
- Windows Defender may slow npm installs — suggest disabling for project directory
- Docker Desktop integration: check `docker info` works from WSL

### Windows (Native / Git Bash / PowerShell)
- Detected when `COMSPEC` or `WINDIR` env vars are set
- Package manager: `choco` or `winget`
- Path separator: backslash
- Shell: PowerShell or cmd — adjust commands accordingly

---

## Sudo Access Check

Always check before suggesting sudo commands:
```bash
sudo -n true 2>/dev/null
# Returns 0 = has passwordless sudo
# Returns 1 = needs password (prompt user) or no sudo access
```

If no sudo access on a VPS:
- Suggest user-level installs only
- nvm, pyenv, rbenv all install to `$HOME` — no sudo needed
- For system packages (nginx, mysql): tell user to run manually with sudo or as root

---

## Package Manager Priority

Use in this order when multiple are available:
1. Existing version manager (nvm, pyenv, rbenv) — always first
2. Homebrew (Mac)
3. apt/apt-get (Debian/Ubuntu)
4. dnf (Fedora/RHEL 8+)
5. yum (CentOS/RHEL 7)
6. pacman (Arch)
7. choco (Windows)
8. winget (Windows — fallback)

---

## Common Edge Cases

### nvm installed but not in current shell
```bash
# nvm needs to be sourced — check common locations
[ -s "$HOME/.nvm/nvm.sh" ] && source "$HOME/.nvm/nvm.sh"
[ -s "/usr/local/opt/nvm/nvm.sh" ] && source "/usr/local/opt/nvm/nvm.sh"  # brew location
```

### pyenv installed but python not using it
```bash
# Check if pyenv shims are in PATH
echo $PATH | grep -q ".pyenv/shims" || echo "pyenv shims not in PATH — run: eval \"\$(pyenv init -)\""
```

### Port already in use
```bash
lsof -i :[port] 2>/dev/null | head -5
# or
ss -tlnp | grep :[port]
```
Always suggest an alternative port if the default is taken.

### npm permission errors (Linux without nvm)
System Node often requires sudo for global installs. Solution: never use global installs — always use npx or local installs.

### PHP version conflicts (multiple PHP versions via apt)
```bash
# Check active PHP version
php -v
# List available
update-alternatives --list php 2>/dev/null
# Switch
sudo update-alternatives --set php /usr/bin/php8.2
```

### Composer not on PATH after install
```bash
# Composer self-installs to ~/bin or ~/.local/bin on Linux
export PATH="$HOME/.composer/vendor/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
```

<#
.SYNOPSIS
  SuperAgents init script - Detect & Install Skills, MCPs, Plugins
.DESCRIPTION
  Phase 1: Detect 7 tools installation status
  Phase 2: Install missing items (needs confirmation or --yes)
  Phase 3: Write memory/tools-state.json
.PARAMETER Yes
  Skip all confirmations, auto-install missing items
.PARAMETER NoInstall
  Detect only, write tools-state.json without installing
.EXAMPLE
  .\init.ps1          # Ask per item
  .\init.ps1 --yes    # Auto
  .\init.ps1 --no-install  # Detect only
#>

param(
  [switch]$Yes,
  [switch]$NoInstall
)

$ErrorActionPreference = "Stop"
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillRoot = "$env:USERPROFILE\.agents\skills"

# ---------- Package manager detection ----------
$pkgMgr = if (Get-Command pnpm -ErrorAction SilentlyContinue) { "pnpm" } else { "npm" }
$uvFound = (Get-Command uv -ErrorAction SilentlyContinue) -ne $null
Write-Host "   Package manager: $pkgMgr  $(if($uvFound){'+ uv'}else{'(uv not found)'})`n" -ForegroundColor DarkGray

# ---------- Output helpers ----------
function Write-Status {
  param([string]$Label, [string]$Message, [string]$Status)
  $icons = @{ ok = "[+]"; miss = "[-]"; info = "[>]"; skip = "[s]"; warn = "[!]" }
  $color = @{ ok = "Green"; miss = "Red"; info = "Cyan"; skip = "Yellow"; warn = "Magenta" }
  Write-Host ("{0} {1,-22} {2}" -f $icons[$Status], $Label, $Message) -ForegroundColor $color[$Status]
}

function Confirm-Step {
  param([string]$Title)
  if ($Yes) { return $true }
  $response = Read-Host "  Install $($Title)? [Y/n]"
  return ($response -eq '' -or $response -eq 'y' -or $response -eq 'Y')
}

function Get-CliVersion {
  param([string]$Command)
  try {
    $result = Invoke-Expression $Command 2>&1 | Out-String
    $line = ($result -split "`n" | Select-Object -First 1).Trim()
    return $line
  } catch { return $null }
}

# ---------- Phase 1: Detection ----------
Write-Host "`n=== Phase 1: Detect installed tools ===`n" -ForegroundColor Cyan

$tools = @{}
$allInstalled = $true

# 1. karpathy-guidelines (skill)
$kpPath = "$skillRoot\karpathy-guidelines\SKILL.md"
$kpFound = Test-Path $kpPath
$kpStatus = "missing"
if ($kpFound) { $kpStatus = "installed" }
$tools["karpathy-guidelines"] = @{
  type="skill"; status=$kpStatus
  version=$null; latest_version=$null; version_checked_at=$null
  source="https://github.com/multica-ai/andrej-karpathy-skills"
  path=$kpPath; last_verified=(Get-Date -Format "yyyy-MM-dd")
}
$kpLabel = "karpathy-guidelines"
if ($kpFound) { Write-Status $kpLabel "installed" "ok" } else { Write-Status $kpLabel "missing" "miss"; $allInstalled = $false }

# 2. skillx (skill + CLI)
$sxPath = "$skillRoot\skillx\SKILL.md"
$sxSkillFound = Test-Path $sxPath
$sxStatus = "missing"
if ($sxSkillFound) { $sxStatus = "installed" }
$sxCliVersion = Get-CliVersion "npx --yes skillx --version 2`$null"
if ($sxCliVersion -and $sxCliVersion -match '(\d[\d.]+\d)') { $sxCliVersion = $Matches[1] }
$tools["skillx"] = @{
  type="skill"; status=$sxStatus
  version=$sxCliVersion; latest_version=$sxCliVersion; version_checked_at=if($sxCliVersion){(Get-Date -Format "yyyy-MM-dd")}else{$null}
  source="https://github.com/nextlevelbuilder/skillx"
  path=$sxPath; last_verified=(Get-Date -Format "yyyy-MM-dd")
}
$sxMsg = "skill:$(if($sxSkillFound){'Y'}else{'N'}) cli:$(if($sxCliVersion){'v'+$sxCliVersion}else{'-'})"
if ($sxSkillFound) { Write-Status "skillx" $sxMsg "ok" } else { Write-Status "skillx" $sxMsg "miss"; $allInstalled = $false }

# 3. ui-ux-pro-max (skill)
$uiPath = "$skillRoot\ui-ux-pro-max\SKILL.md"
$uiFound = Test-Path $uiPath
$uiStatus = "missing"
if ($uiFound) { $uiStatus = "installed" }
$uiVersion = Get-CliVersion "npx --yes ui-ux-pro-max-cli --version 2`$null"
if ($uiVersion -and $uiVersion -match '(\d[\d.]+\d)') { $uiVersion = $Matches[1] }
$tools["ui-ux-pro-max"] = @{
  type="skill"; status=$uiStatus
  version=$uiVersion; latest_version=$uiVersion; version_checked_at=if($uiVersion){(Get-Date -Format "yyyy-MM-dd")}else{$null}
  source="https://github.com/nextlevelbuilder/ui-ux-pro-max-skill"
  path=$uiPath; last_verified=(Get-Date -Format "yyyy-MM-dd")
}
$uiMsg = "skill:$(if($uiFound){'Y'}else{'N'}) cli:$(if($uiVersion){'v'+$uiVersion}else{'-'})"
if ($uiFound) { Write-Status "ui-ux-pro-max" $uiMsg "ok" } else { Write-Status "ui-ux-pro-max" $uiMsg "miss"; $allInstalled = $false }

# 4. context7 (MCP)
$ctxVersion = Get-CliVersion "npx --yes ctx7 --version 2`$null"
$ctxStatus = "missing"
$ctxMsg = "missing"
if ($ctxVersion) { $ctxStatus = "installed"; $ctxMsg = "v$ctxVersion" }
$tools["context7"] = @{
  type="mcp"; status=$ctxStatus
  version=$ctxVersion; latest_version=$ctxVersion; version_checked_at=if($ctxVersion){(Get-Date -Format "yyyy-MM-dd")}else{$null}
  source="https://github.com/upstash/context7"
  path=$null; last_verified=(Get-Date -Format "yyyy-MM-dd")
}
if ($ctxVersion) { Write-Status "context7" $ctxMsg "ok" } else { Write-Status "context7" "missing" "miss"; $allInstalled = $false }

# 5. codebase-memory-mcp (MCP)
$cbmRaw = Get-CliVersion "codebase-memory-mcp --version 2`$null"
$cbmVersion = $null
if ($cbmRaw -and $cbmRaw -match '(\d[\d.]+\d)') { $cbmVersion = $Matches[1] }
$cbmStatus = "missing"
$cbmMsg = "missing"
if ($cbmVersion) { $cbmStatus = "installed"; $cbmMsg = "v$cbmVersion" }
$tools["codebase-memory-mcp"] = @{
  type="mcp"; status=$cbmStatus
  version=$cbmVersion; latest_version=$cbmVersion; version_checked_at=if($cbmVersion){(Get-Date -Format "yyyy-MM-dd")}else{$null}
  source="https://github.com/DeusData/codebase-memory-mcp"
  path=$null; last_verified=(Get-Date -Format "yyyy-MM-dd")
}
if ($cbmVersion) { Write-Status "codebase-memory-mcp" $cbmMsg "ok" } else { Write-Status "codebase-memory-mcp" "missing" "miss"; $allInstalled = $false }

# 6. opencode-wakatime (plugin)
$ocConfig = "$env:USERPROFILE\.config\opencode\opencode.json"
$wkFound = $false
if (Test-Path $ocConfig) {
  $ocJson = Get-Content $ocConfig -Raw | ConvertFrom-Json
  if ($ocJson.plugin -match "wakatime") { $wkFound = $true }
}
$wkStatus = "missing"
if ($wkFound) { $wkStatus = "installed" }
$tools["opencode-wakatime"] = @{
  type="plugin"; status=$wkStatus
  version=$null; latest_version=$null; version_checked_at=$null
  source="https://github.com/angristan/opencode-wakatime"
  path=$ocConfig; last_verified=(Get-Date -Format "yyyy-MM-dd")
}
if ($wkFound) { Write-Status "opencode-wakatime" "installed" "ok" } else { Write-Status "opencode-wakatime" "missing" "miss"; $allInstalled = $false }

# 7. superpowers (framework)
$spCache = "$env:USERPROFILE\.cache\opencode\packages"
$spFound = $false
if (Test-Path $spCache) {
  $spDirs = Get-ChildItem "$spCache\superpowers@*" -Directory -ErrorAction SilentlyContinue
  if ($spDirs) { $spFound = $true }
}
$spStatus = "missing"
if ($spFound) { $spStatus = "installed" }
$tools["superpowers"] = @{
  type="framework"; status=$spStatus
  version=$null; latest_version=$null; version_checked_at=$null
  source="https://github.com/obra/superpowers"
  path=$null; last_verified=(Get-Date -Format "yyyy-MM-dd")
}
if ($spFound) { Write-Status "superpowers" "installed" "ok" } else { Write-Status "superpowers" "missing" "miss"; $allInstalled = $false }

# ---------- Summary ----------
$installedCount = ($tools.Values | Where-Object { $_.status -eq "installed" }).Count
$missingCount = ($tools.Values | Where-Object { $_.status -eq "missing" }).Count
$colorSummary = "Green"
if ($missingCount -gt 0) { $colorSummary = "Yellow" }
Write-Host "`n   Installed: $installedCount  |  Missing: $missingCount`n" -ForegroundColor $colorSummary

# ---------- Phase 2: Install (if needed) ----------
if ($NoInstall) {
  Write-Host "=== --no-install mode, skip installation ===`n" -ForegroundColor Yellow
} elseif ($missingCount -eq 0) {
  Write-Host "=== All tools installed, nothing to do ===`n" -ForegroundColor Green
} else {
  Write-Host "=== Phase 2: Install missing items ===`n" -ForegroundColor Cyan

  # 2a. karpathy-guidelines
  $tool = $tools["karpathy-guidelines"]
  if ($tool.status -eq "missing" -and (Confirm-Step "karpathy-guidelines")) {
    Write-Status "Install" "karpathy-guidelines -> $skillRoot" "info"
    $target = "$skillRoot\karpathy-guidelines"
    if (-not (Test-Path $target)) { New-Item -ItemType Directory -Path $target -Force | Out-Null }
    git clone --depth 1 "https://github.com/multica-ai/andrej-karpathy-skills.git" "$env:TEMP\_sp_kp" 2>$null
    $srcSkill = "$env:TEMP\_sp_kp\skills\karpathy-guidelines"
    if (Test-Path $srcSkill) {
      Copy-Item "$srcSkill\*" $target -Recurse -Force
    } else {
      Copy-Item "$env:TEMP\_sp_kp\CLAUDE.md" "$target\SKILL.md" -Force -ErrorAction SilentlyContinue
    }
    Remove-Item "$env:TEMP\_sp_kp" -Recurse -Force -ErrorAction SilentlyContinue
    $newStatus = "missing"
    if (Test-Path "$target\SKILL.md") { $newStatus = "installed" }
    $tool.status = $newStatus
    Write-Status "Result" $tool.status (if($tool.status -eq "installed"){"ok"}else{"warn"})
  }

  # 2b. skillx
  $tool = $tools["skillx"]
  if ($tool.status -eq "missing" -and (Confirm-Step "skillx")) {
    Write-Status "Install" "skillx -> $skillRoot" "info"
    $target = "$skillRoot\skillx"
    if (-not (Test-Path $target)) { New-Item -ItemType Directory -Path $target -Force | Out-Null }
    git clone --depth 1 "https://github.com/nextlevelbuilder/skillx.git" "$env:TEMP\_sp_sx" 2>$null
    $srcSkill = "$env:TEMP\_sp_sx\.claude\skills\skillx"
    if (Test-Path $srcSkill) {
      Copy-Item "$srcSkill\*" $target -Recurse -Force
    }
    Remove-Item "$env:TEMP\_sp_sx" -Recurse -Force -ErrorAction SilentlyContinue
    $newStatus = "missing"
    if (Test-Path "$target\SKILL.md") { $newStatus = "installed" }
    $tool.status = $newStatus
    Write-Status "Result" $tool.status (if($tool.status -eq "installed"){"ok"}else{"warn"})
  }

  # 2c. ui-ux-pro-max
  $tool = $tools["ui-ux-pro-max"]
  if ($tool.status -eq "missing" -and (Confirm-Step "ui-ux-pro-max")) {
    Write-Status "Install" "ui-ux-pro-max CLI ($pkgMgr)" "info"
    & $pkgMgr install -g ui-ux-pro-max-cli 2>$null
    Write-Status "Init" "uipro init --ai opencode" "info"
    uipro init --ai opencode 2>$null
    $newStatus = "missing"
    if (Test-Path "$skillRoot\ui-ux-pro-max\SKILL.md") { $newStatus = "installed" }
    $tool.status = $newStatus
    Write-Status "Result" $tool.status (if($tool.status -eq "installed"){"ok"}else{"warn"})
  }

  # 2d. context7
  $tool = $tools["context7"]
  if ($tool.status -eq "missing" -and (Confirm-Step "context7")) {
    Write-Status "Install" "context7 MCP (npx ctx7 setup)" "info"
    npx --yes ctx7 setup --opencode 2>$null
    $newVersion = Get-CliVersion "npx --yes ctx7 --version 2`$null"
    $newStatus = "missing"
    if ($newVersion) { $newStatus = "installed"; $tool.version = $newVersion; $tool.latest_version = $newVersion }
    $tool.status = $newStatus
    Write-Status "Result" $tool.status (if($tool.status -eq "installed"){"ok"}else{"warn"})
  }

  # 2e. codebase-memory-mcp
  $tool = $tools["codebase-memory-mcp"]
  if ($tool.status -eq "missing" -and (Confirm-Step "codebase-memory-mcp")) {
    Write-Status "Install" "codebase-memory-mcp (install.ps1)" "info"
    try {
      Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.ps1" -OutFile "$env:TEMP\_cbm_install.ps1"
      Unblock-File "$env:TEMP\_cbm_install.ps1" -ErrorAction SilentlyContinue
      & "$env:TEMP\_cbm_install.ps1" 2>$null
    } catch { Write-Status "Install failed" $_.Exception.Message "warn" }
    Remove-Item "$env:TEMP\_cbm_install.ps1" -Force -ErrorAction SilentlyContinue
    $newVersion = Get-CliVersion "codebase-memory-mcp --version 2`$null"
    $newStatus = "missing"
    if ($newVersion) { $newStatus = "installed"; $tool.version = $newVersion; $tool.latest_version = $newVersion }
    $tool.status = $newStatus
    Write-Status "Result" $tool.status (if($tool.status -eq "installed"){"ok"}else{"warn"})
  }

  # 2f. opencode-wakatime
  $tool = $tools["opencode-wakatime"]
  if ($tool.status -eq "missing" -and (Confirm-Step "opencode-wakatime")) {
    Write-Status "Install" "opencode-wakatime ($pkgMgr)" "info"
    & $pkgMgr install -g opencode-wakatime 2>$null
    Write-Status "Setup" "opencode-wakatime --install" "info"
    opencode-wakatime --install 2>$null
    $wkPluginPath = "$env:USERPROFILE\.config\opencode\plugins\wakatime.js"
    $newStatus = "missing"
    if (Test-Path $wkPluginPath) { $newStatus = "installed" }
    $tool.status = $newStatus
    Write-Status "Result" $tool.status (if($tool.status -eq "installed"){"ok"}else{"warn"})
  }

  # 2g. superpowers
  $tool = $tools["superpowers"]
  if ($tool.status -eq "missing" -and (Confirm-Step "superpowers")) {
    Write-Status "Install" "superpowers (Opencode INSTALL.md)" "info"
    $installUrl = "https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md"
    Write-Status "Guide" "Follow $installUrl to install manually" "info"
    Start-Process $installUrl
    $tool.status = "manual"
  }
}

# ---------- Phase 3: Write tools-state.json ----------
Write-Host "`n=== Phase 3: Write memory/tools-state.json ===`n" -ForegroundColor Cyan
$memoryDir = "$scriptRoot\memory"
if (-not (Test-Path $memoryDir)) { New-Item -ItemType Directory -Path $memoryDir -Force | Out-Null }
$tasksFile = "$memoryDir\tasks.md"
if (-not (Test-Path $tasksFile)) { Set-Content $tasksFile "# Tasks`n`n## Backlog`n`n## In Progress`n`n## Completed`n" -Encoding UTF8 }

$state = @{
  last_updated = Get-Date -Format "yyyy-MM-dd"
  tools = $tools
}
$state | ConvertTo-Json -Depth 4 | Set-Content "$memoryDir\tools-state.json" -Encoding UTF8
Write-Status "Written" "$memoryDir\tools-state.json" "ok"

# ---------- Done ----------
Write-Host "`n=== Done ===`n" -ForegroundColor Green
Write-Host "Installed: $installedCount / 7" -ForegroundColor Green
if ($missingCount -gt 0) {
  Write-Host "Missing: $missingCount (run .\init.ps1 --yes or install manually)" -ForegroundColor Yellow
}

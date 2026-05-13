[Setup]
AppName=SentinelX SOC
AppVersion=2.0
AppPublisher=Davi Vasques - Hacker Ético
DefaultDirName={pf}\SentinelX SOC
DefaultGroupName=SentinelX SOC
OutputDir=installer
OutputBaseFilename=SentinelX_SOC_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes

[Files]
; Executável principal
Source: "dist\SentinelX_SOC.exe"; DestDir: "{app}"; Flags: ignoreversion

; (Opcional mas recomendado) cria pasta data para evitar erros
Source: "data\*"; DestDir: "{app}\data"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\SentinelX SOC"; Filename: "{app}\SentinelX_SOC.exe"
Name: "{commondesktop}\SentinelX SOC"; Filename: "{app}\SentinelX_SOC.exe"

[Run]
Filename: "{app}\SentinelX_SOC.exe"; Description: "Abrir SentinelX SOC"; Flags: nowait postinstall skipifsilent
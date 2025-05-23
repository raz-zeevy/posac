; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Posac"
#define MyAppVersion "{param:MyAppVersion|1.1.8.0}"
#define VersionInfoVersion "{param:MyAppVersion|1.1.8.0}"
#define MyAppPublisher "Raz Zeevy"
#define MyAppURL "https://raz-zeevy.github.io/posac/"
#define MyAppExeName "Posac.exe"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ".pos"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt
#define SessionIcon "lib\assets\icon.ico"

[Setup]
AppId={{A5033936-6373-4BCB-AE0E-231D3E51F329}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
VersionInfoVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={userappdata}\{#MyAppName}
DisableDirPage=yes
ChangesAssociations=yes
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=no
OutputBaseFilename=PosacSetup
OutputDir=releases
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";

[Files]
Source: "dist\Posac\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\Posac\*"; DestDir: "{app}";  Flags: ignoreversion recursesubdirs createallsubdirs

[Registry]
Root: HKCU; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCU; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKCU; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".lss"; ValueData: ""
Root: HKCU; Subkey: ".mmp"; ValueType: string; ValueName: ""; ValueData: "PosacSession"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "PosacSession"; ValueType: string; ValueName: "";ValueData: "Posac Session"; Flags: uninsdeletekey
Root: HKCU; Subkey: "PosacSession\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: """{#SessionIcon}"""
Root: HKCU; Subkey: "PosacSession\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: runascurrentuser nowait postinstall skipifsilent


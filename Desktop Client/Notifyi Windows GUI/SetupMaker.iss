; -- Example1.iss --
; Demonstrates copying 3 files and creating an icon.

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName=Notifyi
AppVersion=1.0
WizardStyle=modern
DefaultDirName={autopf}\Notifyi
DefaultGroupName=Notifyi
UninstallDisplayIcon={app}\notifyi_installer.exe
Compression=lzma2
SolidCompression=yes
OutputDir= Release
WizardSmallImageFile=imagefiles\wizardimage.bmp,imagefiles\wizardimage1.bmp
SetupIconFile = imagefiles\notifyi_icon.ico
OutputBaseFilename=NotifyiDesktopInstaller


[Files]
Source: "SetupFiles/Notifyi.exe"; DestDir: "{app}"  
Source: "SetupFiles/NotifyiUserManager.exe"; DestDir: "{app}"
Source: "SetupFiles/AppConfig.dat"; DestDir:"{localappdata}\Notifyi"
Source: "SetupFiles/userdata.dat"; DestDir: "{localappdata}\Notifyi"

[icons]
Name: "{group}\Notifyi User Manager"; Filename: "{app}\NotifyiUserManager.exe"; 

[Code]

function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  { look for the path with leading and trailing semicolon }
  { Pos() returns 0 if not found }
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;

function FileReplaceString(const FileName, SearchString, ReplaceString: string):boolean;
var
  MyFile : TStrings;
  MyText : string;
begin
  MyFile := TStringList.Create;

  try
    result := true;

    try
      MyFile.LoadFromFile(FileName);
      MyText := MyFile.Text;

      { Only save if text has been changed. }
      if StringChangeEx(MyText, SearchString, ReplaceString, True) > 0 then
      begin;
        MyFile.Text := MyText;
        MyFile.SaveToFile(FileName);
      end;
    except
      result := false;
    end;
  finally
    MyFile.Free;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  Dirname: String;
  LocalDir:String;
begin
if CurStep = ssPostInstall then
  begin
    Dirname := ExpandConstant('{app}');
    LocalDir := ExpandConstant('{localappdata}');
    StringChangeEx(LocalDir, '\', '/', True);
    Log(Dirname)

    FileReplaceString(LocalDir+'\Notifyi\AppConfig.dat', 'LOCALDATADIRPATH', LocalDir+'/Notifyi/')
   end
end;

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; \
    Check: NeedsAddPath(ExpandConstant('{app}'))
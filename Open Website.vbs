Set objShell = WScript.CreateObject("WScript.Shell")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
objShell.CurrentDirectory = strPath

' Build frontend if dist is missing
Set fso = CreateObject("Scripting.FileSystemObject")
If Not fso.FolderExists(strPath & "\frontend\dist") Then
    objShell.Run "cmd /c cd /d """ & strPath & "\frontend"" && npm run build", 0, True
End If

' Start uvicorn hidden (no terminal)
If fso.FileExists(strPath & "\.venv\Scripts\python.exe") Then
    pyCmd = """" & strPath & "\.venv\Scripts\python.exe"" -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
Else
    pyCmd = "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
End If
objShell.Run pyCmd, 0, False

' Wait for server then open browser
WScript.Sleep 3000
objShell.Run "http://localhost:8000", 1, False

Set objShell = Nothing

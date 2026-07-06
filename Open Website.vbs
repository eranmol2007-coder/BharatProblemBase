Set objShell = WScript.CreateObject("WScript.Shell")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
objShell.CurrentDirectory = strPath

Set fso = CreateObject("Scripting.FileSystemObject")

' Build frontend if dist is missing
If Not fso.FolderExists(strPath & "\frontend\dist") Then
    objShell.Run "cmd /c cd /d """ & strPath & "\frontend"" && npm run build", 0, True
End If

' Check if server is already running on port 8000
serverRunning = False
Set objExec = objShell.Exec("cmd /c netstat -ano | findstr :8000")
output = objExec.StdOut.ReadAll()
If InStr(output, "LISTENING") > 0 Then
    serverRunning = True
End If

' Start uvicorn if not already running
If Not serverRunning Then
    If fso.FileExists(strPath & "\.venv\Scripts\python.exe") Then
        pyCmd = """" & strPath & "\.venv\Scripts\python.exe"" -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
    Else
        pyCmd = "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
    End If
    objShell.Run pyCmd, 0, False

    ' Poll until server is ready (up to 30 seconds)
    ready = False
    For i = 1 To 30
        WScript.Sleep 1000
        Set objCheck = objShell.Exec("cmd /c netstat -ano | findstr :8000")
        checkOutput = objCheck.StdOut.ReadAll()
        If InStr(checkOutput, "LISTENING") > 0 Then
            ready = True
            Exit For
        End If
    Next
End If

objShell.Run "http://localhost:8000", 1, False

Set objShell = Nothing

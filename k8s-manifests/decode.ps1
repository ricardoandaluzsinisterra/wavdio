$encodedString = "WURsSE1hV1dkSQ=="
$decodedBytes = [System.Convert]::FromBase64String($encodedString)
$decodedString = [System.Text.Encoding]::UTF8.GetString($decodedBytes)
Write-Output $decodedString
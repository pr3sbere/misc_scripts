<#
Use this script to recursively look for text in a word document.
This script is looking for "Findings" Inside previous Pentest reports.
Updated 10/14/2026
#>
Add-Type -AssemblyName System.IO.Compression.FileSystem
$path    = "C:\Users\tars\Documents\001_Engagements"
$keyword = "Coercion"  # Change this to the finding!

Get-ChildItem $path -Recurse -Filter *.docx -File | Where-Object { $_.Name -notlike '~$*' } | ForEach-Object {
    try {
        $zip   = [IO.Compression.ZipFile]::OpenRead($_.FullName)
        $entry = $zip.GetEntry("word/document.xml")
        $text  = (New-Object IO.StreamReader($entry.Open())).ReadToEnd() -replace '<[^>]+>', ''
        if ($text -match [regex]::Escape($keyword)) { "Found in: $($_.FullName)" }
    } catch { Write-Warning "Skipped: $($_.FullName)" }
    finally { if ($zip) { $zip.Dispose() } }
}
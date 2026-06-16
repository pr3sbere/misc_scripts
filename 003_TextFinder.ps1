<#
Use this script to recursively look for text in a word document.
This script is looking for "Findings" Inside previous Pentest reports.
#>

$path = "C:\Users\tars\Documents\001_Engagements"
$keyword = "Finding Name We're Looking For"  # Change this to the finding!

$word = New-Object -ComObject Word.Application
$word.Visible = $false

Get-ChildItem -Path $path -Recurse -Include *.doc,*.docx | ForEach-Object {
    $doc = $null
    try {
        $doc = $word.Documents.Open($_.FullName, $false, $true) # Open read-only
        if ($doc.Content.Text -match [regex]::Escape($keyword)) {
            Write-Output "Found in: $($_.FullName)"
        }
    } catch {
        # Ignore files that fail to open
    } finally {
        if ($doc -ne $null) { $doc.Close() }
    }
}

$word.Quit()#>

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

$docs = Get-ChildItem -Path "d:\RegAi\cdsco\03_MASTER PROCEDURES" -Include *.doc, *.docx -Recurse

foreach ($doc in $docs) {
    if ($doc.Name -notmatch "^\~") { # Ignore temporary lock files
        $pdfPath = $doc.FullName -replace "\.docx?$", ".pdf"
        if (-not (Test-Path $pdfPath)) {
            Write-Host "Converting: $($doc.FullName)"
            try {
                $document = $word.Documents.Open($doc.FullName, $false, $true) # path, confirmconversions, readonly
                $document.SaveAs([ref] $pdfPath, [ref] 17) # 17 is wdFormatPDF
                $document.Close([ref] 0) # 0 is wdDoNotSaveChanges
            } catch {
                Write-Host "Error converting $($doc.FullName): $_"
            }
        } else {
            Write-Host "Skipping, PDF already exists: $pdfPath"
        }
    }
}

$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
Write-Host "Conversion complete."

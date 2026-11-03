param (
    [string]$docxPath,
    [string]$pdfPath
)

$fullDocx = [System.IO.Path]::GetFullPath($docxPath)
$fullPdf = [System.IO.Path]::GetFullPath($pdfPath)

Write-Host "Opening Word application..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = [Microsoft.Office.Interop.Word.WdAlertLevel]::wdAlertsNone

try {
    Write-Host "Opening document: $fullDocx"
    $doc = $word.Documents.Open($fullDocx)
    Write-Host "Exporting to PDF: $fullPdf"
    $doc.ExportAsFixedFormat($fullPdf, 17) # 17 = wdExportFormatPDF
    $doc.Close([Microsoft.Office.Interop.Word.WdSaveOptions]::wdDoNotSaveChanges)
    Write-Host "Conversion completed successfully!"
}
catch {
    Write-Error $_
}
finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}

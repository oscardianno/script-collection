# Define parameters
param(
    [string]$TargetDate = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss"), # Default to current date
    [string]$TargetDirectory = "."                                   # Default to current directory
)

# Convert the target date to a DateTime object
try {
    $Date = [DateTime]::Parse($TargetDate)
} catch {
    Write-Error "Invalid date format. Please use 'YYYY-MM-DDTHH:MM:SS'."
    exit 1
}

# Get all files in the target directory
$Files = Get-ChildItem -Path $TargetDirectory -File -Recurse

if ($Files.Count -eq 0) {
    Write-Output "No files found in the directory: $TargetDirectory"
    exit 0
}

# Update timestamps for each file
foreach ($File in $Files) {
    try {
        $File.CreationTime = $Date
        $File.LastWriteTime = $Date
        Write-Output "Updated: $($File.FullName)"
    } catch {
        Write-Error "Failed to update timestamps for file: $($File.FullName). $_"
    }
}

Write-Output "Timestamps updated for all files in $TargetDirectory."

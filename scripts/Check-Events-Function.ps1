function Check-Events {
    <#
    .SYNOPSIS
        Look up one or more events in a .evtx file by their EventRecordID.

    .DESCRIPTION
        Wraps Get-WinEvent with an XPath filter per RecordID, so you can pass a
        batch of anomalous EventRecordIDs (e.g. from your anomaly_score results)
        and get readable output for each.

    .PARAMETER RecordId
        One or more EventRecordID values to look up.

    .PARAMETER LogPath
        Path to the .evtx file. Required, must be passed explicitly every time,
        no default is used.

    .EXAMPLE
        Check-Events -RecordId 2899035, 2899036, 2899101 -LogPath "C:\data\raw\93_applog.evtx"

    .EXAMPLE
        Get-Content .\anomalous_ids.txt | Check-Events -LogPath "C:\data\raw\93_applog.evtx"
    #>
    param(
        [Parameter(Mandatory = $true, Position = 0, ValueFromPipeline = $true)]
        [long[]]$RecordId,

        [Parameter(Mandatory = $true)]
        [string]$LogPath
    )

    begin {
        if (-not (Test-Path $LogPath)) {
            Write-Error "Log file not found: $LogPath"
            return
        }

        $allIds = @()
    }

    process {
        $allIds += $RecordId
    }

    end {
        foreach ($id in $allIds) {
            Write-Host ""
            Write-Host "=== EventRecordID $id ===" -ForegroundColor Cyan

            $xpath = "*[System[EventRecordID=$id]]"

            try {
                $event = Get-WinEvent -Path $LogPath -FilterXPath $xpath -ErrorAction Stop
            }
            catch {
                Write-Host "  No event found for EventRecordID $id" -ForegroundColor Yellow
                continue
            }

            $event | Select-Object TimeCreated, Id, LevelDisplayName, ProviderName, Message |
                Format-List
        }
    }
}

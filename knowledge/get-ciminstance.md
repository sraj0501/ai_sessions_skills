# Get Ciminstance

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## System Information

### Retrieve hardware details for the video controller
<!-- sig: 09b0906c0103 -->

```bash
Get-CimInstance Win32_VideoController | Select-Object Name,AdapterRAM,DriverVersion | Format-List
```

- **What it does:** Queries the WMI CIM class for video controller hardware and selects the Name, AdapterRAM, and DriverVersion properties, displaying them in a list format.
- **Why:** Provides a structured way to audit GPU hardware specifications and driver versions directly from the PowerShell console.
- **Example:** Get-CimInstance Win32_VideoController | Select-Object Name,AdapterRAM,DriverVersion | Format-List
- **Notes:** Requires administrative privileges to access certain hardware properties depending on the system configuration.

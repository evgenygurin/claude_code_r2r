## Telemetry

R2R uses telemetry to collect **anonymous** usage information. This data helps understand how R2R is used, prioritize new features and bug fixes, and improve overall performance and stability.

### Introduction

R2R uses telemetry to collect **anonymous** usage information. This data helps understand how R2R is used, prioritize new features and bug fixes, and improve overall performance and stability.

### Disabling Telemetry

To opt out of telemetry, set an environment variable:

```bash
export TELEMETRY_ENABLED=false
```

**Valid Values**: `false`, `0`, `f`

When telemetry is disabled, no events are captured.

### Collected Information

Our telemetry system collects basic, anonymous information such as:

- **Feature Usage**: Which features are being used and their frequency.
- **Performance Metrics**: Query latencies, system resource usage.
- **Error Logs**: Information about errors and exceptions.

### Telemetry Data Storage

*Details about telemetry data storage are not provided in the original document.*

### Why We Collect Telemetry

Telemetry data helps us:

1. Understand which features are most valuable to users.
2. Identify areas for improvement.
3. Prioritize development efforts.
4. Enhance R2R’s overall performance and stability.

We appreciate your participation in our telemetry program, as it directly contributes to making R2R better for everyone.

### Conclusion

Telemetry in R2R provides valuable insights into system usage and performance, enabling continuous improvement. Users concerned about privacy can easily disable telemetry by setting the appropriate environment variable.

---
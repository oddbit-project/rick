# Software Bill of Materials (SBOM)

This directory contains automatically generated SBOM files for the rick project.

## Files

- **sbom-cyclonedx.json** - CycloneDX format SBOM in JSON
- **sbom-cyclonedx.xml** - CycloneDX format SBOM in XML
- **sbom-spdx.json** - SPDX format SBOM in JSON
- **sbom-spdx.spdx** - SPDX format SBOM in tag-value format

## Generation

SBOMs are automatically generated and updated by the GitHub Actions workflow (`.github/workflows/sbom.yml`) on:
- Every push to the `master` branch
- Every release
- Manual workflow dispatch

## Formats

### SPDX (Software Package Data Exchange)
SPDX is an ISO/IEC standard (ISO/IEC 5962:2021) for communicating software bill of materials information.

### CycloneDX
CycloneDX is a lightweight SBOM standard designed for use in application security contexts and supply chain component analysis.

## Usage

These SBOM files can be used for:
- Supply chain security analysis
- License compliance verification
- Vulnerability tracking
- Dependency auditing
- Software composition analysis

## Tools

The SBOMs are generated using:
- **cyclonedx-bom** - Official CycloneDX Python tool
- **sbom4python** - Multi-format SBOM generator supporting both SPDX and CycloneDX

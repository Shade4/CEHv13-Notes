# 03 — Internet Research Services

Internet research services aggregate public information from many sources.

## People-search services

These services can expose information such as:

- Names
- Professional history
- Public contact information
- Locations
- Public associations

For security work, the important lesson is that attackers can combine small pieces of public information.

## Job sites

Job advertisements are valuable sources of technology intelligence.

A job listing may mention:

- Programming languages
- Cloud providers
- Databases
- Operating systems
- CI/CD platforms
- Security products
- Monitoring tools
- Frameworks

### Example

If a public job advertisement repeatedly asks for experience with a particular technology stack, that may be a useful **hypothesis** about the organization's technology environment.

It is not proof.

## Public documents

Useful document sources include:

- Annual reports
- Technical presentations
- Conference slides
- Whitepapers
- Press releases
- Procurement documents
- Job descriptions

Documents may reveal:

- Internal terminology
- Employee names
- Technology names
- Office locations
- Business processes
- File metadata

## Dark-web footprinting

Dark-web research is a specialized OSINT activity.

Potential defensive objectives include:

- Identifying leaked organizational credentials
- Detecting stolen documents
- Monitoring mentions of an organization
- Understanding breach exposure

This area carries substantial legal, privacy, and safety considerations. Do not purchase stolen data, interact with criminal services, or attempt to access illicit systems.

## Competitive intelligence

Competitive intelligence is the lawful collection and analysis of information about competitors or market participants.

Sources can include:

- Financial reports
- Press releases
- Public presentations
- Patent databases
- Job advertisements
- Public websites
- News articles
- Industry publications

The ethical distinction is important:

**Competitive intelligence uses legitimate sources and analysis. It is not a license for unauthorized intrusion, theft, or deception.**

## Correlation

The strongest value comes from combining sources.

Example:

```text
Job advertisement
      ↓
Technology clue
      ↓
Public documentation
      ↓
Subdomain naming pattern
      ↓
DNS record
      ↓
Hosting/provider clue
```

Each step should be recorded separately so that assumptions are not mistaken for facts.

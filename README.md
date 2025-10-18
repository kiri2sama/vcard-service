# vCard Service

A simple vCard.link clone for creating and sharing digital business cards.

## Features

- Create digital business cards with contact information
- Generate shareable URLs
- Download vCard (.vcf) files
- Simple and clean interface

## Installation

```bash
pip3 install flask
```

## Usage

```bash
python3 app.py
```

Server runs on http://localhost:6509

## API Endpoints

- `GET /` - Create vCard form
- `POST /api/vcards` - Create new vCard
- `GET /c/{slug}` - View vCard
- `GET /api/vcards/{slug}/download` - Download VCF file

## License

MIT

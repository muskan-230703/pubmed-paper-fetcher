# PubMed Paper Fetcher

## Description
This command-line tool fetches research papers from PubMed based on a user-provided query and filters out papers with at least one non-academic author affiliated with a pharmaceutical or biotech company.

## Features
- Query PubMed with full search syntax
- Identify non-academic authors using affiliation/email heuristics
- CSV output or print to console
- Modular, typed code with Poetry setup

## Installation

```bash
git clone https://github.com/muskan-230703/pubmed-paper-fetcher
cd pubmed-paper-fetcher
poetry install
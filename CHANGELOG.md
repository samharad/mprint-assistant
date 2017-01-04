# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) 
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]
### Added

### Changed
- Fixed a typo in PrintSession.authenticate, where a useless variable "prompt" was set
- Removed "import json", since the request module's built-in .json() function is used for parsing
- Added catch block for ValueError, thrown when JSON cannot be parsed from server response

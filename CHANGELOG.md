# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog] and this project adheres to [Semantic Versioning].

  [Keep a Changelog]: http://keepachangelog.com/en/1.0.0/
  [Semantic Versioning]: http://semver.org/spec/v2.0.0.html

## [0.4.3] - 2023-02-14

### Fixed
- when using `return_offers()` while searching, we correctly parse the datetime for
  payment_requirements - previously this would raise

  [0.4.3]: https://github.com/duffelhq/duffel-api-python/releases/tag/0.4.3

## [0.4.2] - 2023-02-13

### Added
- new search flow called multi-step search - more on our [guide]
- examples on how to use the multi-step search flow

  [0.4.2]: https://github.com/duffelhq/duffel-api-python/releases/tag/0.4.2
  [guide]: https://duffel.com/docs/guides/multi-step-search

## [0.4.1] - 2023-01-25

### Added
- `max_connections` parameter to `OfferRequest`

  [0.4.1]: https://github.com/duffelhq/duffel-api-python/releases/tag/0.4.1

## [0.4.0] - 2022-02-11

### Added

- `content` field to `Order`s

### Changed

- Changed API versions from `beta` to `v1`
- Various library version updates

  [0.4.0]: https://github.com/duffelhq/duffel-api-python/releases/tag/0.4.0

## [0.3.1] - 2022-02-11

### Fixed
- Set `payment_required_by` and `price_guarantee_expires_at` fields on
  `Offer.PaymentRequirements` as nullable.

  [0.3.1]: https://github.com/duffelhq/duffel-api-python/releases/tag/0.3.1

## [0.3.0] - 2022-02-01

### Added
- Added a changelog.
- Added GitHub issue templates.
- Added contribution code of conduct guidelines.
- Added type annotations to model classes.
- Added example of searching and booking using a combination of adult and infant
  passengers.

  [0.3.0]: https://github.com/duffelhq/duffel-api-python/releases/tag/0.3.0

### Fixed
- Updated date parsing to use `fromisoformat()`.
- Updated string interpolation to use f-strings.

## [0.2.0] - 2022-01-07

### Added
- Added support and testing for Python 3.10.

### Fixed
- Updated classes and methods to fix type related errors.

### Removed
- Removed support and testing for Python 3.6.

  [0.2.0]: https://github.com/duffelhq/duffel-api-python/releases/tag/0.2.0

## [0.1.0] - 2021-12-31

### Added
- Initial release.

  [0.1.0]: https://github.com/duffelhq/duffel-api-python/releases/tag/0.1.0

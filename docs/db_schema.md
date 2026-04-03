# Database Schema Notes

## Core
- `SiteConfiguration`: site title, tagline, and about content.

## Accounts
- `Profile`: one-to-one extension of Django `User` for bio, website, location, and avatar.

## Blog
- `Category`, `Tag`, and `Post` for content management.

## Contact
- `ContactMessage` to store messages from the contact form.
# RegPulse Development Notes

This file contains my development notes throughout the project.
## RegPulse Data Model (Designed Day 2)

Table Name: `circulars`

- id: uuid (Primary Key)
- circular_id: string (unique)
- title: string
- url: string
- publish_date: date
- applicability: string (or array)
- summary: text
- deadline: date (optional)
- obligations: text / json
- scraped_at: timestamp
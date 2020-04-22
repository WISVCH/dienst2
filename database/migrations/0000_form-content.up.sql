BEGIN;

CREATE TABLE "form_content" (
    "id" SERIAL UNIQUE PRIMARY KEY,
    "gender" varchar NOT NULL,
    "first_name" varchar NOT NULL,
    "last_name" varchar NOT NULL,
    "email" varchar UNIQUE NOT NULL,
    "phone_number" varchar NOT NULL,
    "full_name" varchar NOT NULL,
    "street" varchar NOT NULL,
    "street_number" varchar NOT NULL,
    "postal_code" varchar NOT NULL,
    "place" varchar NOT NULL,
    "country" varchar NOT NULL,
    "letters" varchar NOT NULL,
    "netid" varchar UNIQUE NOT NULL,
    "yearbook_permission" boolean NOT NULL DEFAULT false,
    "activity_mailing" boolean NOT NULL DEFAULT false,
    "career_mailing" boolean NOT NULL DEFAULT false,
    "education_mailing" boolean NOT NULL DEFAULT false,
    "machazine" boolean NOT NULL DEFAULT false,
    "added_to_ldb" boolean NOT NULL DEFAULT false,
    "freshmen_weekend" boolean NOT NULL DEFAULT false,
    "paid_status" varchar,
    "amount_paid" decimal NOT NULL DEFAULT 0.0,
    "created_at" timestamp NOT NULL DEFAULT (now())
);

COMMIT;
package entities

type FormEntity struct {
	Gender string `db:"gender" form:"gender"`
	FirstName string `db:"first_name" form:"first_name"`
	LastName string `db:"last_name" form:"last_name"`
	Email string `db:"email" form:"email"`
	PhoneNumber string `db:"phone_number" form:"phone_number"`
	FullName string `db:"full_name" form:" full_name"`
	StreetName string `db:"street" form:"street_name"`
	StreetNumber string `db:"street_number" form:"street_number"`
	PostalCode string `db:"postal_code" form:"postal_code"`
	Place string `db:"place" form:"place"`
	Country string `db:"country" form:"country"`
	FirstLetters string `db:"letters" form:"first_letters"`
	NetID string `db:"netid" form:"netid"`
	YearBookPer bool `db:"yearbook_permission" form:"yearbook_permission"`
	ActivityMail bool `db:"activity_mailing" form:"activity_mail"`
	CareerMail bool `db:"career_mailing" form:"career_mail"`
	EducationMail bool `db:"education_mailing" form:"education_mail"`
	Machazine bool `db:"machazine" form:"machazine"`
	Added bool `db:"added_to_ldb"`
	FreshMenWeekend bool `db:"freshmen_weekend" form:"freshmen_weekend"`
}
from enum import Enum

from linkedin_api import Linkedin

from ..schema import BaseModel


class Period(BaseModel):
    year: int  # experience > timePeriod > * > year
    month: int = None  # experience > timePeriod > * > month


class TimePeriod(BaseModel):
    start_date: Period  # experience > timePeriod > startDate
    end_date: Period | None = None  # experience > timePeriod > endDate


class EmployeeCountRange(BaseModel):
    start: int  # experience > company > employeeCountRange > start
    end: int  # experience > company > employeeCountRange > end


class Company(BaseModel):
    employee_count_range: EmployeeCountRange  # experience > company > employeeCountRange
    industries: list[str]  # experience > company > industries


class Expirience(BaseModel):
    # job description
    title: str  # experience > title
    description: str  # experience > description
    company_name: str  # experience > companyName
    location_name: str  # experience > locationName
    company: Company  # experience > company


class Education(BaseModel):
    degree_name: str  # education > degreeName
    field_of_study: str  # education > fieldOfStudy
    school_name: str  # education > schoolName
    time_period: TimePeriod  # education > timePeriod


class Certification(BaseModel):
    authority: str  # certifications > authority
    name: str  # certifications > name
    time_period: TimePeriod


class EnumProficiency(str, Enum):
    ELEMENTARY = "ELEMENTARY"  # (Elementary proficiency)
    LIMITED_WORKING = "LIMITED_WORKING"  # (Limited working proficiency)
    PROFESSIONAL_WORKING = "PROFESSIONAL_WORKING"  # (Professional working proficiency)
    FULL_PROFESSIONAL = "FULL_PROFESSIONAL"  # (Full professional proficiency)
    NATIVE_OR_BILINGUAL = "NATIVE_OR_BILINGUAL"  # (Native or bilingual proficiency)


class Language(BaseModel):
    name: str  # name
    proficiency: EnumProficiency  # proficiency


class Skill(BaseModel):
    name: str  # name


class Profile(BaseModel):
    first_name: str  # firstName
    last_name: str  # lastName
    public_id: str  # public_id
    summary: str  # summary
    industry_name: str  # industryName
    headline: str  # headline
    # location
    geo_country_name: str  # locationName
    geo_location_name: str  # geoLocationName
    # experiences
    experience: list[Expirience] | None = None  # experiences > experience
    # educations
    education: list[Education] | None = None  # educations > education
    # languages
    languages: list[Language] | None = None  # languages > language
    # certifications
    certifications: list[Certification] | None = None  # certifications > certification
    # skills
    skills: list[Skill] | None = None  # skills > skill


class LinkedinCrawler:
    def __init__(self, username: str, password: str):
        self.api = Linkedin(username=username, password=password)

    def get_profile(self, public_id: str) -> Profile | None:
        profile = self.api.get_profile(public_id)
        if not profile:
            return None
        return Profile.model_validate(profile)

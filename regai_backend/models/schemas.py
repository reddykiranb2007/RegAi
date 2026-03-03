from pydantic import BaseModel, Field
from typing import List, Optional

class DeviceClassificationRequest(BaseModel):
    device_name: str = Field(..., description="Name of the medical device", example="Infusion Pump")
    intended_use: str = Field(..., description="Intended use or function of the device", example="Used for controlled intravenous infusion of fluids")

class DeviceClassificationResponse(BaseModel):
    device_name: str
    risk_class: str = Field(..., description="CDSCO Risk Class (A, B, C, D)")
    regulatory_pathway: str = Field(..., description="Regulatory pathway for compliance")
    required_documents: List[str] = Field(..., description="List of documents required for submission")
    estimated_timeline_days: str = Field(..., description="Estimated timeline for approval in months/days")
    authority: str = Field(..., description="Regulatory Authority (SLA or CDSCO)")
    match_type: str = Field(..., description="Type of match found (Exact, Fuzzy, AI, Rule-Based)")
    confidence_score: float = Field(..., description="Confidence score of the classification (0.0 - 1.0)")

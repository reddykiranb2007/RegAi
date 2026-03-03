from typing import List, Dict

class RuleEngine:
    """
    Encapsulates the CDSCO specific rules for classification, documentation, and timelines.
    """

    @staticmethod
    def get_rules_for_class(risk_class: str, is_ivd: bool = False) -> Dict:
        """
        Returns the regulatory requirements based on the risk class.
        """
        risk_class = risk_class.upper().strip()
        
        # Base Rules
        rules = {
            "A": {
                "risk_level": "Low Risk",
                "authority": "State Licensing Authority (SLA)",
                "license": "Registration (Form MD-4) / Retention",
                "timeframe": "3-6 Months",
                "documents": [
                    "Device Master File (Basic)",
                    "Plant Master File",
                    "ISO 13485 Certificate (Voluntary but recommended)",
                    "Labels & IFU"
                ]
            },
            "B": {
                "risk_level": "Low-Moderate Risk",
                "authority": "State Licensing Authority (SLA)",
                "license": "Form MD-5 (Manufacture) / MD-15 (Import)",
                "timeframe": "6-9 Months",
                "documents": [
                    "Device Master File (Standard)",
                    "Plant Master File",
                    "ISO 13485 Certificate (Mandatory)",
                    "Clinical Evaluation Report (Literature based)",
                    "Test Reports from NABL Lab"
                ]
            },
            "C": {
                "risk_level": "Moderate-High Risk",
                "authority": "Central Licensing Authority (CDSCO HQ)",
                "license": "Form MD-9 (Manufacture) / MD-15 (Import)",
                "timeframe": "9-12 Months",
                "documents": [
                    "Device Master File (Detailed)",
                    "Plant Master File",
                    "ISO 13485 Certificate",
                    "Clinical Investigation Report / Clinical Evaluation Report",
                    "Risk Management Report (ISO 14971)",
                    "Stability Data",
                    "Biocompatibility Reports"
                ]
            },
            "D": {
                "risk_level": "High Risk",
                "authority": "Central Licensing Authority (CDSCO HQ)",
                "license": "Form MD-9 (Manufacture) / MD-15 (Import)",
                "timeframe": "12-18+ Months",
                "documents": [
                    "Device Master File (Comprehensive)",
                    "Plant Master File",
                    "ISO 13485 Certificate",
                    "Clinical Investigation Data (Pilot & Pivotal)",
                    "Post-Market Surveillance Plan",
                    "Risk Management Report (ISO 14971)",
                    "Biocompatibility & Toxicology Studies"
                ]
            }
        }
        
        return rules.get(risk_class, {
            "risk_level": "Unknown",
            "authority": "Consult Regulatory Expert",
            "license": "Assessment Required",
            "timeframe": "TBD",
            "documents": ["Consult Regulatory Expert"]
        })
    
    @staticmethod
    def determine_class_by_keywords(text: str) -> str:
        """
        Fallback keyword-based classification rule engine.
        """
        text = text.lower()
        
        # High Risk Patterns
        if any(x in text for x in ['implant', 'pacemaker', 'valve', 'defibrillator', 'hiv', 'hepatitis', 'stem cell']):
            return "D"
            
        # Moderate-High Risk Patterns
        if any(x in text for x in ['pump', 'ventilator', 'x-ray', 'ct scanner', 'dialysis', 'catheter']):
            # Usually C, sometimes B depending on invasiveness. Defaulting to C for safety in logic.
            return "C"
            
        # Low-Moderate Patterns
        if any(x in text for x in ['thermometer', 'monitor', 'ultrasound', 'needle', 'syringe', 'analyzer']):
            return "B"
            
        # Default Low Risk
        return "B" # Safe default for software logic if unsure, or "A"

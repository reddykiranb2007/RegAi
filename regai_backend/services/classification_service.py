from .rule_engine import RuleEngine
from .embedding_service import EmbeddingService
from utils.excel_loader import ExcelLoader
from models.schemas import DeviceClassificationResponse

class ClassificationService:
    def __init__(self):
        self.device_data = ExcelLoader.load_device_data()
        self.embedding_service = EmbeddingService()
        
        # Determine if data is List or Dict
        if isinstance(self.device_data, dict):
            self.device_data = list(self.device_data.values())
            
        self.data_map = {d.get('originalName', '').lower(): d for d in self.device_data}

    def classify_device(self, device_name: str, intended_use: str) -> DeviceClassificationResponse:
        
        clean_name = device_name.strip().lower()
        match_type = "Rule-Based"
        confidence = 0.5
        matched_device_entry = None
        
        # 1. Exact Match Strategy
        if clean_name in self.data_map:
            matched_device_entry = self.data_map[clean_name]
            match_type = "Exact Match"
            confidence = 1.0
            
        # 2. Fuzzy/Embedding Strategy (if no exact match)
        if not matched_device_entry:
            fuzzy_result = self.embedding_service.find_best_match(device_name, self.device_data)
            if fuzzy_result:
                matched_device_entry = fuzzy_result['match']
                match_type = "Fuzzy Match"
                confidence = fuzzy_result['score'] / 100.0
        
        # 3. Determine Risk Class
        risk_class = "B" # Default safest median
        
        if matched_device_entry:
            risk_class = matched_device_entry.get('class', 'B')
        else:
            # Fallback to Rule Engine by keywords if no database match found
            risk_class = RuleEngine.determine_class_by_keywords(device_name + " " + intended_use)
            match_type = "Keyword Heuristic"
            confidence = 0.6
            
        # 4. Get Regulatory Rules
        reg_rules = RuleEngine.get_rules_for_class(risk_class)
        
        return DeviceClassificationResponse(
            device_name=matched_device_entry.get('originalName', device_name) if matched_device_entry else device_name,
            risk_class=f"Class {risk_class}",
            regulatory_pathway=reg_rules["license"],
            required_documents=reg_rules["documents"],
            estimated_timeline_days=reg_rules["timeframe"],
            authority=reg_rules["authority"],
            match_type=match_type,
            confidence_score=confidence
        )

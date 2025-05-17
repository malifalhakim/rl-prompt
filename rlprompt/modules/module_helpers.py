from dataclasses import dataclass, field
from typing import Optional

from omegaconf import DictConfig

from rlprompt.modules import SQLModule
from rlprompt.modules.q_module import QModule
from rlprompt.models import BaseModel
from rlprompt.rewards import BaseReward

def make_sql_module(model: BaseModel,
                    reward: BaseReward,
                    config: "DictConfig",
                    target_model: Optional[BaseModel] = None) -> SQLModule:
    return SQLModule(model, target_model, reward, 
                     config.sql_loss_impl, config.training_mode, 
                     config.mix_strategy, config.target_update_method, 
                     config.target_update_steps, config.target_learning_rate, 
                     config.reward_shaping, config.reward_shaping_old_min, 
                     config.reward_shaping_old_max, 
                     config.reward_shaping_new_min, 
                     config.reward_shaping_new_max, 
                     config.top_k, config.top_p, config.num_beams)

def make_q_module(
    model: BaseModel,
    reward_computer: BaseReward, 
    config: "DictConfig",
    target_model: Optional[BaseModel] = None
) -> QModule:
    return QModule(
        model=model,
        target_model=target_model,
        reward_computer=reward_computer,
        gamma=config.gamma,
        target_update_method=config.target_update_method,
        target_update_steps=config.target_update_steps,
        target_learning_rate=config.target_learning_rate,
        reward_shaping=config.reward_shaping,
        reward_shaping_old_min=config.reward_shaping_old_min,
        reward_shaping_old_max=config.reward_shaping_old_max,
        reward_shaping_new_min=config.reward_shaping_new_min,
        reward_shaping_new_max=config.reward_shaping_new_max,
        top_k=config.top_k,
        top_p=config.top_p,
        num_beams=config.num_beams
    )

@dataclass
class SQLModuleConfig:
    sql_loss_impl: str = "v2_v2r_v3_v3r"
    training_mode: str = "sql-onpolicy"
    algorithm: str = "sql-onpolicy"
    mix_strategy: Optional[str] = None
    # Target model setting
    target_update_method: str = "polyak"
    target_update_steps: Optional[int] = None
    target_learning_rate: float = 0.001
    # Reward shaping linearly transforms reward range of [old_min, old_max] to [new_min, new_max]
    reward_shaping: bool = True
    reward_shaping_old_min: float = 0
    reward_shaping_old_max: float = 1
    reward_shaping_new_min: float = 0
    reward_shaping_new_max: float = 5
    # Prompt generation setting
    top_k: Optional[int] = None
    top_p: float = 1.0
    num_beams: int = 1
    # Q learning parameters
    gamma: float = 0.99 # just for compatibility

@dataclass
class QModuleConfig:
    # Q-Learning specific
    algorithm: str = "q-onpolicy"
    gamma: float = 0.99
    
    target_update_method: str = "polyak" 
    target_update_steps: Optional[int] = 100 
    target_learning_rate: float = 0.001 
    
    # Reward shaping
    reward_shaping: bool = True
    reward_shaping_old_min: float = 0
    reward_shaping_old_max: float = 1
    reward_shaping_new_min: float = 0
    reward_shaping_new_max: float = 5
    
    # Prompt generation settings for policy
    top_k: Optional[int] = None
    top_p: float = 1.0
    num_beams: int = 1
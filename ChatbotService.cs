using System;
using System.Threading.Tasks;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Orchestration;
using Microsoft.SemanticKernel.SkillDefinition;
using Microsoft.SemanticKernel.SemanticFunctions;
using System.ComponentModel;

namespace CarnivoreAI
{
    public class CarnivoreChatbot
    {
        private IKernel _kernel;
        private ISKFunction _chatFunction;
        
        public CarnivoreChatbot()
        {
            // Initialize Semantic Kernel
            _kernel = Kernel.Builder
                .WithAzureChatCompletionService(
                    "gpt-4",
                    Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT"),
                    Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY"))
                .Build();
            
            // Define the carnivore diet skill
            string carnivoreSkill = @"
            [SKFunction]
            [Description(""Provides advice about carnivore and ketogenic diets"")]
            public string CarnivoreAdvice(string input)
            {
                return GetCarnivoreResponse(input);
            }
            
            private string GetCarnivoreResponse(string query)
            {
                query = query.ToLower();
                
                if (query.Contains(""what to eat"") || query.Contains(""food""))
                {
                    return ""On carnivore diet, eat: Red meat, organ meats, eggs, fish, poultry. Focus on fatty cuts for energy."";
                }
                else if (query.Contains(""avoid"") || query.Contains(""not eat""))
                {
                    return ""Avoid: Sugar, grains, seed oils, processed foods, high-oxalate vegetables, alcohol."";
                }
                else if (query.Contains(""benefit"") || query.Contains(""why""))
                {
                    return ""Benefits: Weight loss, reduced inflammation, stable energy, mental clarity, improved digestion, autoimmune relief."";
                }
                else if (query.Contains(""vitamin d"") || query.Contains(""winter""))
                {
                    return ""In winter, supplement with Vitamin D3 (5000-10000 IU) + K2 (100mcg). Get from fatty fish and egg yolks."";
                }
                else
                {
                    return ""The carnivore diet focuses on animal foods only. It eliminates plants to reduce inflammation and optimize health."";
                }
            }";
            
            // Create the semantic function
            var promptConfig = new PromptTemplateConfig
            {
                Description = "Carnivore diet advisor",
                Completion = new PromptTemplateConfig.CompletionConfig
                {
                    MaxTokens = 500,
                    Temperature = 0.3,
                    TopP = 0.5
                }
            };
            
            var promptTemplate = new PromptTemplate(
                carnivoreSkill,
                promptConfig,
                _kernel
            );
            
            _chatFunction = _kernel.CreateSemanticFunction(
                promptTemplate,
                skillName: "CarnivoreDiet",
                functionName: "Advise",
                description: "Provides carnivore diet advice"
            );
        }
        
        public async Task<string> GetResponse(string userInput)
        {
            try
            {
                var context = new SKContext();
                context["input"] = userInput;
                
                var result = await _kernel.RunAsync(context, _chatFunction);
                return result.Result;
            }
            catch (Exception ex)
            {
                return $"I encountered an error: {ex.Message}";
            }
        }
    }
    
    public class CarnivoreSkills
    {
        [SKFunction("Generate meal plan for carnivore diet")]
        [SKFunctionInput(Description = "Number of days for meal plan")]
        public string GenerateMealPlan(int days)
        {
            var plan = $"{days}-Day Carnivore Meal Plan:\n\n";
            
            for (int i = 1; i <= days; i++)
            {
                plan += $"Day {i}:\n";
                plan += "Breakfast: 4 eggs + 4 bacon slices\n";
                plan += "Lunch: 8oz ground beef patties (2)\n";
                plan += "Dinner: 12oz ribeye steak + butter\n";
                plan += "Snack: Pork rinds or hard cheese\n\n";
                plan += "Or stick One Meal A day\n";
            }
            
            return plan;
        }
        
        [SKFunction("Calculate macros for carnivore meal")]
        [SKFunctionInput(Description = "Food items separated by comma")]
        public string CalculateMacros(string foods)
        {
            // Simplified macro calculation
            return $"For {foods}: Estimated 75% fat, 20% protein, 5% carbs (from eggs/dairy if included).";
        }
    }
}

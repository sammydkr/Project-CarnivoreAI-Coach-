using System;
using System.Threading.Tasks;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Orchestration;
using Azure;
using Azure.AI.OpenAI;

namespace CarnivoreAI
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("🥩 DIKER CarnivoreAI Coach - C# Backend");
            Console.WriteLine("==================================");
            
            var chatbot = new CarnivoreChatbot();
            
            while (true)
            {
                Console.Write("\nYou: ");
                var userInput = Console.ReadLine();
                
                if (userInput?.ToLower() == "exit") break;
                
                var response = await chatbot.GetResponse(userInput);
                Console.WriteLine($"\nCarnivoreAI: {response}");
            }
        }
    }
}

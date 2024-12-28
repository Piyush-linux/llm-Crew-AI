# CrewAI Project

Welcome to the **CrewAI Project**! This project leverages the powerful CrewAI framework to define agents and tasks for automating workflows in a structured, extensible manner. The code demonstrates a `Crewbot` implementation, showcasing agents and tasks designed for curriculum design, resource curation, and progress tracking.

## Features

- **Agents**: Modular and reusable components for specific tasks like curriculum design, resource curation, and progress tracking.
- **Tasks**: Structured workflows with output files for efficient task management.
- **Crew**: A collection of agents and tasks executed in a sequential or hierarchical process.
- **Customizable Configuration**: YAML-based configuration files for agents and tasks for easy customization.

## File Structure

```yml
.
crewbot/
├── .venv
├── knowledge/
├── src
│   ├── crewbot
│   │   ├── config/
│   │   │   ├── agents.yml 
│   │   │   ├── tasks.yml
│   │   ├── main.py # Entry point for the Crewbot implementation
│   │   ├── crew.py
├── .venv
├── .gitignore # Ignore unnecessary files and directories
├── README.md
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-github-username>/crewai-project.git
   cd crewai-project
   ```

2. Install dependencies:
   ```bash
   pip install crewai
   ```

## Usage

1. Configure agents and tasks using YAML files in the `config/` directory.
2. Run the Crewbot implementation:
   ```bash
   
   ```

## Key Concepts

### Agents

Agents are autonomous units in the CrewAI ecosystem. In this project, agents are configured in `agents.yaml` and can be extended using tools as per requirements.

- Example agent setup:
  ```python
  @agent
  def curriculum_designer(self) -> Agent:
      return Agent(
          config=self.agents_config['curriculum_designer'],
          verbose=True
      )
  ```

### Tasks

Tasks define specific actions performed by agents. Outputs are saved to files for review and further use.

- Example task setup:
  ```python
  @task
  def design_curriculum(self) -> Task:
      return Task(
          config=self.tasks_config['design_curriculum'],
          output_file='design_curriculum.md'
      )
  ```

### Crew

The Crew groups agents and tasks and manages their execution order using a `Process`.

- Example crew setup:
  ```python
  @crew
  def crew(self) -> Crew:
      return Crew(
          agents=self.agents,
          tasks=self.tasks,
          process=Process.sequential,
          verbose=True
      )
  ```

## Documentation

- [CrewAI Concepts: Crews](https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators)
- [CrewAI Concepts: Agents](https://docs.crewai.com/concepts/agents#yaml-configuration-recommended)
- [CrewAI Concepts: Tasks](https://docs.crewai.com/concepts/tasks#overview-of-a-task)

## Contributing

Contributions are welcome! Feel free to fork this repository, make changes, and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Author
Developed by [Piyush](https://github.com/Piyuhs-linux).

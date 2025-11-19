## Orchestration

Orchestration in R2R is managed using [Hatchet](https://docs.hatchet.run/home), a distributed, fault-tolerant task queue that handles complex workflows such as ingestion and knowledge graph construction.

### Key Concepts

| Concept          | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **Workflows**    | Sets of functions executed in response to external triggers.               |
| **Workers**      | Long-running processes that execute workflow functions.                    |
| **Managed Queue**| Low-latency queue for handling real-time tasks.                            |

### Orchestration in R2R

#### Benefits of Orchestration

1. **Scalability**: Efficiently handles large-scale tasks.
2. **Fault Tolerance**: Built-in retry mechanisms and error handling.
3. **Flexibility**: Easy to add or modify workflows as R2R’s capabilities expand.

#### Workflows in R2R

1. **IngestFilesWorkflow**: Handles file ingestion, parsing, chunking, and embedding.
2. **UpdateFilesWorkflow**: Manages updating existing files.
3. **KgExtractAndStoreWorkflow**: Extracts and stores knowledge graph information.
4. **CreateGraphWorkflow**: Orchestrates knowledge graph creation.
5. **EnrichGraphWorkflow**: Handles graph enrichment processes like node creation and clustering.

### Orchestration GUI

Access the Hatchet front-end application at [http://localhost:7274](http://localhost:7274).

#### Login

Use the following credentials to log in:

- **Email**: admin@example.com
- **Password**: Admin123!!

![Logging into Hatchet](https://files.buildwithfern.com/https://sciphi.docs.buildwithfern.com/2024-12-13T18:29:49.890Z/images/hatchet_login.png)

#### Running Tasks

After initiating tasks like `r2r documents create-samples`, view running workflows:

![Running Workflows](https://files.buildwithfern.com/https://sciphi.docs.buildwithfern.com/2024-12-13T18:29:49.890Z/images/hatchet_running.png)

#### Inspecting a Workflow

Inspect and manage individual workflows, including retrying failed jobs:

![Inspecting a Workflow](https://files.buildwithfern.com/https://sciphi.docs.buildwithfern.com/2024-12-13T18:29:49.890Z/images/hatchet_workflow.png)

#### Long Running Tasks

Hatchet supports long-running tasks, essential for processes like graph construction.

![Long Running Tasks](https://files.buildwithfern.com/https://sciphi.docs.buildwithfern.com/2024-12-13T18:29:49.890Z/images/hatchet_long_running.png)

### Coming Soon

Details about upcoming orchestration features will be available soon.

### Best Practices

1. **Development**:
   - Start with small document sets.
   - Test with single documents first.
   - Scale gradually to larger collections.

2. **Performance**:
   - Monitor community size and complexity.
   - Use pagination for large result sets.
   - Consider breaking very large collections.

3. **Quality**:
   - Review community summaries.
   - Validate findings accuracy.
   - Monitor retrieval relevance.

### Troubleshooting

**Common Issues and Solutions:**

1. **Unable to Create/Modify Collections**:
   - Ensure the user has superuser privileges.

2. **User Not Seeing Collection Content**:
   - Verify that the user is correctly added to the collection.
   - Ensure documents are properly assigned.

3. **Performance Issues with Large Collections**:
   - Use pagination when retrieving users or documents.
   - Consider splitting large collections.

### Conclusion

Orchestration via Hatchet enables R2R to handle complex and large-scale workflows efficiently. By leveraging workflows and monitoring tools, you can ensure smooth and scalable operations within your R2R deployment.

---
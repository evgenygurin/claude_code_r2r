## Web Development

Web developers can easily integrate R2R into their projects using the [R2R JavaScript client](https://github.com/SciPhi-AI/r2r-js). For extensive references and examples, explore the [R2R Application](https://r2r-docs.sciphi.ai/cookbooks/application) and its source code.

### Hello R2R—JavaScript

R2R offers configurable vector search and RAG capabilities with direct method calls.

#### Example: `r2r-js/examples/hello_r2r.js`

```javascript
const { r2rClient } = require("r2r-js");

const client = new r2rClient("http://localhost:7272");

async function main() {
    const files = [
        { path: "examples/data/raskolnikov.txt", name: "raskolnikov.txt" },
    ];

    const EMAIL = "admin@example.com";
    const PASSWORD = "change_me_immediately";

    console.log("Logging in...");
    await client.users.login(EMAIL, PASSWORD);

    console.log("Ingesting file...");
    const documentResult = await client.documents.create({
        file: { path: "examples/data/raskolnikov.txt", name: "raskolnikov.txt" },
        metadata: { title: "raskolnikov.txt" },
    });

    console.log("Document result:", JSON.stringify(documentResult, null, 2));

    console.log("Performing RAG...");
    const ragResponse = await client.rag({
        query: "What does the file talk about?",
        rag_generation_config: {
            model: "openai/gpt-4.1",
            temperature: 0.0,
            stream: false,
        },
    });

    console.log("Search Results:");
    ragResponse.results.search_results.chunk_search_results.forEach(
        (result, index) => {
            console.log(`\nResult ${index + 1}:`);
            console.log(`Text: ${result.metadata.text.substring(0, 100)}...`);
            console.log(`Score: ${result.score}`);
        },
    );

    console.log("\nCompletion:");
    console.log(ragResponse.results.completion.choices[0].message.content);
}

main();
```

### r2r-js Client

#### Installing

Install the R2R JavaScript client using [npm](https://www.npmjs.com/package/r2r-js):

```bash
npm install r2r-js
```

#### Creating the Client

First, create the R2R client and specify the base URL where the R2R server is running.

```javascript
const { r2rClient } = require("r2r-js");

// http://localhost:7272 or your R2R server address
const client = new r2rClient("http://localhost:7272");
```

#### Log into the Server

Authenticate the session using default superuser credentials.

```javascript
const EMAIL = "admin@example.com";
const PASSWORD = "change_me_immediately";

console.log("Logging in...");
await client.users.login(EMAIL, PASSWORD);
```

#### Ingesting Files

Specify and ingest files.

```javascript
const file = { path: "examples/data/raskolnikov.txt", name: "raskolnikov.txt" };

console.log("Ingesting file...");
const ingestResult = await client.documents.create({
    file: { path: "examples/data/raskolnikov.txt", name: "raskolnikov.txt" },
    metadata: { title: "raskolnikov.txt" },
});

console.log("Ingest result:", JSON.stringify(ingestResult, null, 2));
```

**Sample Output:**

```json
{
  "results": {
    "processed_documents": [
      "Document 'raskolnikov.txt' processed successfully."
    ],
    "failed_documents": [],
    "skipped_documents": []
  }
}
```

#### Performing RAG

Make a RAG request.

```javascript
console.log("Performing RAG...");
const ragResponse = await client.rag({
    query: "What does the file talk about?",
    rag_generation_config: {
        model: "openai/gpt-4.1",
        temperature: 0.0,
        stream: false,
    },
});

console.log("Search Results:");
ragResponse.results.search_results.chunk_search_results.forEach(
    (result, index) => {
        console.log(`\nResult ${index + 1}:`);
        console.log(`Text: ${result.metadata.text.substring(0, 100)}...`);
        console.log(`Score: ${result.score}`);
    },
);

console.log("\nCompletion:");
console.log(ragResponse.results.completion.choices[0].message.content);
```

**Sample Output:**

```
Performing RAG...

Search Results:

Result 1:
Text: praeterire culinam eius, cuius ianua semper aperta erat, cogebatur. Et quoties praeteribat,...

Score: 0.08281802143835804

Result 2:
Text: In vespera praecipue calida ineunte Iulio iuvenis e cenaculo in quo hospitabatur in S. loco exiit et...

Score: 0.052743945852283036

...

Completion:
The file discusses the experiences and emotions of a young man who is staying in a small room in a tall house.
He is burdened by debt and feels anxious and ashamed whenever he passes by the kitchen of his landlady, whose
door is always open [1]. On a particularly warm evening in early July, he leaves his room and walks slowly towards
a bridge, trying to avoid encountering his landlady on the stairs. His room, which is more like a closet than a
proper room, is located under the roof of the five-story house, while the landlady lives on the floor below and
provides him with meals and services [2].
```

### Connecting to a Web App

Integrate R2R into web applications by creating API routes and React components.

#### Setting up an API Route

Create `r2r-query.ts` in the `pages/api` directory to handle R2R queries.

#### Frontend: React Component

Create a React component, e.g., `index.tsx`, to interact with the API route, providing an interface for user queries and displaying results.

#### Template Repository

For a complete working example, check out the [R2R Web Dev Template Repository](https://github.com/SciPhi-AI/r2r-webdev-template).

**Usage:**

1. **Clone the Repository:**

```bash
git clone https://github.com/SciPhi-AI/r2r-webdev-template.git
cd r2r-webdev-template
```

2. **Install Dependencies:**

```bash
pnpm install
```

3. **Run the Development Server:**

Ensure your R2R server is running, then start the frontend:

```bash
pnpm dev
```

Access the dashboard at [http://localhost:3000](http://localhost:3000).

### Best Practices

1. **Secure API Routes**: Ensure API routes are protected and validate user input.
2. **Optimize Frontend Performance**: Lazy load components and manage state efficiently.
3. **Handle Errors Gracefully**: Provide user-friendly error messages and fallback options.
4. **Implement Caching**: Cache frequent queries to reduce load and improve response times.
5. **Maintain Consistent State**: Synchronize frontend state with backend data to prevent discrepancies.

### Conclusion

The R2R JavaScript client simplifies integration into web applications, enabling developers to build powerful RAG features with minimal setup. Utilize the template repository for a quick start and explore more advanced examples in the [R2R Dashboard](https://github.com/SciPhi-AI/R2R-Application).

---
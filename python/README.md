# Python

Run the application with:

```
python contacts.py <number of contacts>
```

Commit at insert

| size         | final commit (in ms) | inline commit (in ms) | batch commit (in ms)
|--------------|--------------|--------------|-------------|
| 10           | 0m0.029s     | 0m0.084s     | 10          |
| 100          | 0m0.032s     | 0m0.489s     | 10          |
| 500          | 0m0.041s     | 0m2.294s     | 10          |
| 1000         | 0m0.042s     | 0m4.586s     | 10          |
| 5000         | 0m0.055s     | 0m24.211s    | 10          |
| 10,000       | 0m0.069s     | 0m46.346s    | 10          |
| 50,000       | 0m0.190s     | 3m54.275s    | 10   s       |
| 100,000      | 0m0.339s     | x            | 10          |
| 1,000,000    | 0m3.338s     | x            | 10          |
| 10,000,000   | 0m32.453s    | x            | 10          |
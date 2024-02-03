# Domain Modeling

+---------------------+
|      Main Screen    |
|    - Update Checker |
+---------------------+
          |
          v
+---------------------+
| Hardware Information|
|    - Display system |
|      information    |
+---------------------+
          |
          v
+---------------------+
|  Check for Updates  |
|    - Get user       |
|      consent        |
|    - Determine OS   |
|      - Windows      |
|        - Scrape for |
|          updates     |
|      - macOS         |
|        - Scrape for |
|          updates     |
|      - Linux         |
|        - Execute     |
|          update cmd  |
|      - Unsupported   |
|        - Display     |
|          message     |
|    - Open browser    |
|      (optional)      |
+---------------------+
          |
          v
+---------------------+
|Check Software Updates|
|   - Get installed    |
|     packages         |
|   - Check for updates|
|   - Display results  |
+---------------------+
          |
          v
+---------------------+
| Choose Log Location |
|   - Open directory   |
|     selection        |
|   - Update log file  |
|     locations        |
+---------------------+
          |
          v
+---------------------+
|       Logging       |
|   - Log update      |
|     history         |
|   - Log errors       |
+---------------------+
          |
          v
+---------------------+
|    Custom Dialogs   |
|   - Display various |
|     dialogs (e.g.,   |
|     update info,     |
|     user consent,    |
|     software updates,|
|     log location)    |
+---------------------+

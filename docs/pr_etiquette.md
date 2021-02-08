# PR Comment Etiquette

With every PR comment you should prepend with one of the following etiquette tags to help the reader understand the meaning of your comment.
This helps separate something like "Change this now or it'll break!" vs. "I prefer if this variable was named snake_case".

## Etiquette Tags

| Tag Name | Meaning | Example |
| --- | --- | --- |
| Change | This is an error that has to change. Either it will break the code or it strongly violates existing conventions. The normal PR comment. | > Change: This will have a syntax error on the first call.<br>> Change: This variable is a typo and will give a Syntax Error. |
| Question | A question about how the code works or why a decision was made. | > Question: Where does this value come from? |
| Concern | A serious concern about the change. Typically this is a change that is too large to be made through individual "Change" comments. | > Concern: Instead of handling empty cases at every function call we should make sure that this other function can never return empty cases. |
| Discussion | This is note that does not have a clear solution. This might not have originated from this change but is something that you might discuss offline afterwards. | > Discussion: I wonder if we should be caching these results in the database instead of calculating them at runtime. Would having to manage cache invalidation be too much work for the gains? |
| Praise | Compliment your peer on something well written or something that taught you a new thing. | > Praise: This is great! I didn't know you could use that built-in function for this. |
| Suggestion | A well meant suggestion that might involve additional "out-of-scope" work. Take it or leave it. | > Suggestion: We should refactor these to use a common base class since there are so many duplicates now. |
| Nitpick | A minor point that does not change the behavior but is against best practices enough that you think it should change. | > Nitpick: I think you should use tabs instead of spaces for just this file<br>> Nitpick: In the docstring you should use 'their' instead of 'there'. |
| Guide | A helpful PR, typically from the PR creator or a domain expert, that is meant to help understand what the related code hunk is trying to do. This is the "opposite" of a Question comment should be written in place where you'd expect someone to have questions. | > Guide: This section is copy-pasted from https....<br>> Guide: The `>>` operator has a special meaning here and it does ... |

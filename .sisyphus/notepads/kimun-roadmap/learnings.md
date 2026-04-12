Handled anuncio delivery by filtering published items from the last 24 hours and targeting enrolled users when a course is attached.
Added calendar sync for Anuncio via generic post_save/post_delete receivers in calendario/signals.py; sender checks avoid circular imports while keeping event cleanup tied to publication state and deletion.
Implemented at-risk student reporting by reusing dashboard query logic in a shared helper and exposing it through both the admin dashboard context and a management command.
4. Created `static/css/kimun.css` as a standalone redesign layer with spacing/radius/shadow tokens, refined component variants, stagger/float/pulse animations, and motion-reduction coverage without touching the shared base template styles.

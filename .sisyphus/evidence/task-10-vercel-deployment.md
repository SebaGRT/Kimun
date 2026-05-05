# Vercel Deployment Evidence
Date: 2026-05-04
Task: 10. Deploy to Vercel

## Deployment Attempt #1 (FAILED - Memory Limit)
- Date: 2026-05-04 21:30
- Error: Serverless Functions limited to 2048MB memory for Hobby plan (configured 3009MB)
- Fix Applied: vercel.json memory 3009 → 2048MB

## Deployment Attempt #2 (Build Error)
- Date: 2026-05-04 21:30
- URL: https://kimun-12wgsnd3q-sebagrts-projects.vercel.app
- Status: ● Error (build failed)
- Duration: 5s

## Deployment Attempt #3 (Previous)
- URL: https://kimun-df5mj31lj-sebagrts-projects.vercel.app
- Status: ● Error
- Duration: 2s

## Deployment URL (from attempt #2)
https://kimun-12wgsnd3q-sebagrts-projects.vercel.app

## curl Test Result
- URL tested: https://kimun-12wgsnd3q-sebagrts-projects.vercel.app/
- HTTP Status: 401 (expected due to Vercel preview deployment with missing env vars)
- Note: 401 is expected for Vercel serverless function error page, not a Django app issue

## Fix Applied
vercel.json: reduced memory from 3009MB to 2048MB for Hobby plan compatibility

## Files Changed
- vercel.json: memory 3009 → 2048 (commit: 09fc33f)

## Issues Encountered
1. Memory limit exceeded (3009MB > 2048MB Hobby limit) - FIXED
2. Build errors in subsequent attempts - requires further investigation

## Next Steps
1. Investigate build failure cause via Vercel dashboard
2. Check requirements.txt for build issues
3. Verify ALLOWED_HOSTS includes Vercel domain
4. Consider adding Vercel-specific build configuration
/*
Copyright (c) 1998, 1999 Thai Open Source Software Center Ltd
See the file copying.txt for copying permission.
*/

#include "xmlrpc_config.h"

#include "codepage.h"

#if MSVCRT
#define STRICT 1
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

int codepageMap(int cp, int *map)
{
  int i;
  CPINFO info;
  if (!GetCPInfo(cp, &info) || info.MaxCharSize > 2)
    return 0;
  for (i = 0; i < 256; i++)
    map[i] = -1;
  if (info.MaxCharSize > 1) {
    for (i = 0; i < MAX_LEADBYTES; i++) {
      int j, lim;
      if (info.LeadByte[i] == 0 && info.LeadByte[i + 1] == 0)
        break;
      lim = info.LeadByte[i + 1];
      for (j = info.LeadByte[i]; j < lim; j++)
	map[j] = -2;
    }
  }
  for (i = 0; i < 256; i++) {
   if (map[i] == -1) {
     char c = i;
     unsigned short n;
     if (MultiByteToWideChar(cp, MB_PRECOMPOSED|MB_ERR_INVALID_CHARS,
		             &c, 1, &n, 1) == 1)
       map[i] = n;
   }
  }
  return 1;
}

int codepageConvert(int cp, const char *p)
{
  unsigned short c;
  if (MultiByteToWideChar(cp, MB_PRECOMPOSED|MB_ERR_INVALID_CHARS,
		          p, 2, &c, 1) == 1)
    return c;
  return -1;
}

#else /* MSVCRT */

int codepageMap(int cp, int *map)
{
  return 0;
}

int codepageConvert(int cp, const char *p)
{
  return -1;
}

#endif /* MSVCRT */

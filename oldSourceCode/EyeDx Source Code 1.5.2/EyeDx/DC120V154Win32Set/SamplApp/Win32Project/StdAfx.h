// stdafx.h : include file for standard system include files,//  or project specific include files that are used frequently, but//      are changed infrequently//#define VC_EXTRALEAN		// Exclude rarely-used stuff from Windows headers#include <afxwin.h>         // MFC core and standard components#include <afxext.h>         // MFC extensions   #ifndef _AFX_NO_AFXCMN_SUPPORT#include <afxcmn.h>			// MFC support for Windows 95 Common Controls#endif // _AFX_NO_AFXCMN_SUPPORT//****************************************************// + Ohbe#include <windowsx.h>#ifdef ALLSTAR//#include "kdc4pw.h"#else//#include "kdc25.h"// + Ogawa//#include "dc20_50.h"#include "dc120.h"// - Ogawa#endif#include "dither.h" // + Ohbe DeleteMode is defined. here.typedef short DC20DeleteMode;// - Ohbe//****************************************************
/*******************************************************************************\ CEyeDxPreferences - a class for managing preferences for the EyeDx program, based on the CPreferenceMgr class by Dan Crevier, 6/9/97\*******************************************************************************/#ifndef _H_CEyeDxPreferences#define _H_CEyeDxPreferences#pragma once#if defined(__CFM68K__) && !defined(__USING_STATIC_LIBS__)	#pragma import on#endifclass LFileStream;class LStr255;#include <PP_Prefix.h>#include "CPreferencesMgr.h"class CEyeDxPreferences : public CPreferenceMgr{	public:		CEyeDxPreferences();		virtual CEyeDxPreferences();					protected:		virtual void SetDefaultPreferences() = 0;		virtual void Read(LFileStream &prefFile) = 0;		virtual void Write(LFileStream &prefFile) = 0;		virtual void ReportError(const LStr255 &errorString);		private:			OSType	browserChoice;};#if defined(__CFM68K__) && !defined(__USING_STATIC_LIBS__)	#pragma import reset#endif#endif //_H_CPreferenceMgr
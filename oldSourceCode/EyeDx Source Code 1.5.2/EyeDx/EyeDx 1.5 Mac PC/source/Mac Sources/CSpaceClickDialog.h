// =================================================================================//	CSpaceClickDialog.h	// =================================================================================//	CSpaceClickDialog.cp	#pragma once#include <LGADialog.h>class CSpaceClickDialog : public LGADialog {public:	enum { class_ID = 'SclD' };								CSpaceClickDialog( LStream *inStream );								~CSpaceClickDialog();		virtual Boolean		HandleKeyPress(								const EventRecord&	inKeyEvent);								protected:};
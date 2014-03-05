// =================================================================================//	CDialogClick.cp					�1995-1998  Metrowerks Inc. All rights reserved.// =================================================================================//	CDialogClick.h	#include <LCommander.h>#include <LWindow.h>#include <PP_Messages.h>#include <UDesktop.h>#include "CDialogClickAttachment.h"// =================================================================================//	CDialogClickAttachment// =================================================================================// ---------------------------------------------------------------------------------//		� CDialogClickAttachment// ---------------------------------------------------------------------------------CDialogClickAttachment::CDialogClickAttachment(	LWindow	*theParentWindow )		: LAttachment( msg_Click, true ){	mParentWindow = theParentWindow;	mMessage = msg_Event; // We only handle this message}// ---------------------------------------------------------------------------------//		� ~CDialogClickAttachment// ---------------------------------------------------------------------------------CDialogClickAttachment::~CDialogClickAttachment(){}// ---------------------------------------------------------------------------------//		� ExecuteSelf// ---------------------------------------------------------------------------------voidCDialogClickAttachment::ExecuteSelf(	MessageT	inMessage,	void		*ioParam ){	// Turn off host execution by default.	mExecuteHost = false;	// If we're here the user clicked the mouse while the parent dialog is	// visible. Our whole purpose in life is to just send the parent a simulated	// msg_KeyPress that is a Return. This will cause the dialog to simulate hitting	// the default button. This assumes that the buttons themselves handle being clicked	// BEFORE we get called, since us simulating a Return when the user clicks the Cancel	// button isn't very good at all.		if (inMessage == msg_Event)	{		WindowPtr	macWindowP;		SInt16		thePart = ::MacFindWindow(inMacEvent.where, &macWindowP);			if (thePart == inDesk)		// Only happens when a truly modal window									//   is in front and the user clicks on									//   the desktop		}
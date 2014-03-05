// ===========================================================================//	CSingleClickListBox.h					PowerPlant 1.9.3	�1993-1998 Metrowerks Inc.// ===========================================================================#ifndef _H_CSingleClickListBox#define _H_CSingleClickListBox#pragma once#include <LListBox.h>// ---------------------------------------------------------------------------class CSingleClickListBox : public LListBox {public:	enum { class_ID = FOUR_CHAR_CODE('sclb') };						CSingleClickListBox();						CSingleClickListBox(								const CSingleClickListBox		&inOriginal);						CSingleClickListBox(								const SPaneInfo		&inPaneInfo,								Boolean				inHasHorizScroll,								Boolean				inHasVertScroll,								Boolean				inHasGrow,								Boolean				inHasFocusBox,								MessageT			inDoubleClickMessage,								SInt16				inTextTraitsID,								SInt16				inLDEFid,								LCommander			*inSuper);						CSingleClickListBox(								LStream				*inStream);					MessageT			GetSingleClickMessage() const												{ return mSingleClickMessage; }													void				SetSingleClickMessage(								MessageT			inMessage)						{							mSingleClickMessage = inMessage;						}	void				MakeCellVisible(Cell	inCell);	protected:	MessageT		mSingleClickMessage;	virtual void		ClickSelf(								const SMouseDownEvent	&inMouseDown);	};#endif